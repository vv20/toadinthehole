from aws_cdk import Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53
from constructs import Construct

from ..common import Component, Domain, get_environment_domain


class ToadInTheHoleCDNStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.domain_name: str = self.node.try_get_context('domain_name')
        self.stack_environment: str = self.node.try_get_context('environment')
        self.host_at_apex: bool = bool(self.node.try_get_context('host_at_apex'))

        self.lookup_zone()
        self.create_certificate()
        self.create_exports()

    def lookup_zone(self) -> None:
        self.zone: route53.HostedZone = route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=self.domain_name)

    def create_certificate(self) -> None:
        self.certificate: acm.Certificate = acm.Certificate(
                self,
                Component.ENVIRONMENT_CERTIFICATE.get_component_name(self.stack_environment),
                domain_name=get_environment_domain(self.stack_environment, self.domain_name),
                validation=acm.CertificateValidation.from_dns(self.zone))

        self.additional_domains: list[str] | None = None
        if self.host_at_apex:
            self.additional_domains = [self.domain_name]

        self.frontend_certificate: acm.Certificate = acm.Certificate(
                self,
                Component.FRONTEND_CERTIFICATE.get_component_name(self.stack_environment),
                domain_name=Domain.FRONTEND.get_domain_name(self.stack_environment, self.domain_name),
                subject_alternative_names=self.additional_domains,
                validation=acm.CertificateValidation.from_dns(self.zone))
                
    def create_exports(self) -> None:
        self.frontend_certificate_arn: str = self.frontend_certificate.certificate_arn