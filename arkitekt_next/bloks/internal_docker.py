from typing import Dict, Any
import secrets

from arkitekt_next.bloks.lok import LokBlok
from arkitekt_next.bloks.services.gateway import GatewayService
from arkitekt_next.bloks.socket import DockerSocketBlok
from blok import blok, InitContext, ExecutionContext, Option
from blok.bloks.services.dns import DnsService
from blok.tree import YamlFile, Repo


@blok("live.arkitekt.internal_engine")
class InternalDockerBlok:
    def __init__(self) -> None:
        self.host = "internal_docker"
        
        self.image = "jhnnsrs/deployer:0.0.1-vanilla"
        self.instance_id = "INTERNAL_DOCKER"


    def preflight(self, init: InitContext, gateway: GatewayService, lok: LokBlok, socket: DockerSocketBlok):
        for key, value in init.kwargs.items():
            setattr(self, key, value)

        deps = init.dependencies

        if self.skip:
            return

        self._socket = socket.register_socket(self.host)
        self.gateway_host = gateway.get_internal_host()
        self.gateway_port = gateway.get_http_port()

        self.token = lok.retrieve_token()

        self.command = (
           f"arkitekt-next run prod --redeem-token={self.token} --url http://{self.gateway_host}:{self.gateway_port}"
        )

        self.initialized = True

    def build(self, context: ExecutionContext):
        if self.skip:
            return
        db_service = {
            "labels": [
                "fakts.service=io.livekit.livekit",
                "fakts.builder=livekitio.livekit",
            ],
            "image": self.image,
            "command": self.command,
            "volumes": [f"{self._socket}:/var/run/docker.sock"],
            "environment": {
                "INSTANCE_ID": self.instance_id,
            },
        }

        context.docker_compose.set_nested("services", self.host, db_service)

    def get_options(self):
        with_host = Option(
            subcommand="host",
            help="The host of this service",
            default=self.host,
        )
        with_skip = Option(
            subcommand="skip",
            help="Should we skip creating this service?",
            default=False,
            type=bool,
           
        )

        return [
            with_host,
            with_skip,
        ]

    def __str__(self) -> str:
        return (
            f"InterDocker(host={self.host}, command={self.command}, image={self.image})"
        )
