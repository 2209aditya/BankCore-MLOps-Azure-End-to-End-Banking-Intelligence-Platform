import subprocess
from pathlib import Path


def deploy_to_aks(
    manifest_directory="k8s",
):

    directory = Path(manifest_directory)

    manifests = [
        directory / "deployment.yaml",
        directory / "service.yaml",
        directory / "hpa.yaml",
        directory / "ingress.yaml",
    ]

    for manifest in manifests:

        if not manifest.exists():
            raise FileNotFoundError(
                f"Manifest not found: {manifest}"
            )

        subprocess.run(
            [
                "kubectl",
                "apply",
                "-f",
                str(manifest),
            ],
            check=True,
        )


if __name__ == "__main__":

    deploy_to_aks()