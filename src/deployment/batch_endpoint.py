from pathlib import Path


class BatchEndpoint:

    def __init__(
        self,
        model_path: str,
    ):

        self.model_path = Path(
            model_path
        )

    def validate_model(self):

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        return True

    def validate_input(
        self,
        input_path: str,
    ):

        path = Path(input_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Input not found: {path}"
            )

        return True

    def run(
        self,
        input_path: str,
    ):

        self.validate_model()
        self.validate_input(input_path)

        return {
            "status": "ready",
            "model": str(self.model_path),
            "input": str(input_path),
        }