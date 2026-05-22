from typing import Dict, Any, Tuple
from pathlib import Path


class Parser:
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
                    raise ValueError(f"Syntax error on line {line_num}: missing '='")
                
                key, value = clean_line.split("=", 1)
                self.config[key.strip().upper()] = value.strip()

    def get_args(self) -> Tuple[int, int, Tuple[int, int], Tuple[int, int], str, bool, int]:
        """Validates and returns configuration parameters."""
        try:
            width = int(self.config["WIDTH"])
            height = int(self.config["HEIGHT"])
            
            # Парсинг координат (ENTRY=0,0)
            entry_parts = list(map(int, self.config["ENTRY"].split(",")))
            entry = (entry_parts[0], entry_parts[1])
            
            exit_parts = list(map(int, self.config["EXIT"].split(",")))
            exit_coords = (exit_parts[0], exit_parts[1])
            
            output_file = self.config["OUTPUT_FILE"]
            perfect = self.config.get("PERFECT", "True").lower() == "true"
            seed = int(self.config.get("SEED", 0))

            return (width, height, entry, exit_coords, output_file, perfect, seed)
            
        except KeyError as e:
            raise ValueError(f"Missing mandatory key in config: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid parameter format: {e}")
