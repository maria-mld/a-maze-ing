from typing import Dict, Tuple
from pathlib import Path


class Parser:
    """Reads and validates a key-value maze configuration file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.config: Dict[str, str] = {}
        self._load_config()

    def _load_config(self) -> None:
        if not self.file_path.is_file():
            raise FileNotFoundError(f"Config file not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue

                if "=" not in clean_line:
                    raise ValueError("Syntax error on line "
                                     f"{line_num}: missing '='")

                key, value = clean_line.split("=", 1)
                self.config[key.strip().upper()] = value.strip()

    def get_args(self) -> Tuple[int,
                                int,
                                Tuple[int, int],
                                Tuple[int, int],
                                str, bool, int]:
        """Validates and returns configuration parameters."""
        try:
            width = int(self.config["WIDTH"])
            height = int(self.config["HEIGHT"])

            entry = self._parse_coordinate("ENTRY")
            exit_coords = self._parse_coordinate("EXIT")

            output_file = self.config["OUTPUT_FILE"]
            perfect = self.config.get("PERFECT", "True").lower() == "true"
            seed = int(self.config.get("SEED", 0))

            return (width, height, entry,
                    exit_coords, output_file, perfect, seed)

        except KeyError as e:
            raise ValueError(f"Missing mandatory key in config: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid parameter format: {e}")

    def _parse_coordinate(self, key: str) -> Tuple[int, int]:
        """Parse a coordinate value written as x,y."""
        parts = self.config[key].split(",")
        if len(parts) != 2:
            raise ValueError(f"{key} must contain exactly two values: x,y")
        return int(parts[0]), int(parts[1])
