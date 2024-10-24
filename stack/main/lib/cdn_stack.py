from aws_cdk import Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53
from constructs import Construct

from ..common import Component, Domain, get_environment_domain


class ToadInTheHoleCDNStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = self.node.try_get_context('domain_name')
        environment = self.node.try_get_context('environment')
        host_at_apex = bool(self.node.try_get_context('host_at_apex'))
        zone = self.lookup_zone(domain_name)
        frontend_certificate = self.create_certificate(environment, domain_name, zone, host_at_apex)
        self.frontend_certificate_arn = frontend_certificate.certificate_arn

    def lookup_zone(self, domain_name):
        return route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=domain_name)

    def create_certificate(
            self,
            environment,
            domain_name,
            zone,
            host_at_apex):
        acm.Certificate(
                self,
                Component.ENVIRONMENT_CERTIFICATE.get_component_name(environment),
                domain_name=get_environment_domain(environment, domain_name),
                validation=acm.CertificateValidation.from_dns(zone))

        additional_domains = None
        if host_at_apex:
            additional_domains = [domain_name]

        frontend_certificate = acm.Certificate(
                self,
                Component.FRONTEND_CERTIFICATE.get_component_name(environment),
                domain_name=Domain.FRONTEND.get_domain_name(environment, domain_name),
                subject_alternative_names=additional_domains,
                validation=acm.CertificateValidation.from_dns(zone))
        return frontend_certificate
