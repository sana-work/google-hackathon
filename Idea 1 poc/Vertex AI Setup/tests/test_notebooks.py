import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "01_Setup_and_RAG_App.ipynb",
    ROOT / "02_Adversarial_Test_Generator.ipynb",
    ROOT / "03_Evaluation_Pipeline.ipynb",
    ROOT / "04_Auto_Remediation.ipynb",
]


class NotebookMigrationTests(unittest.TestCase):
    def test_notebooks_no_longer_use_deprecated_vertexai_sdk(self):
        for notebook in NOTEBOOKS:
            data = json.loads(notebook.read_text())
            source = "\n".join(
                "".join(cell.get("source", []))
                for cell in data.get("cells", [])
                if cell.get("cell_type") == "code"
            )
            self.assertNotIn("import vertexai", source, notebook.name)
            self.assertNotIn("vertexai.generative_models", source, notebook.name)
            self.assertIn("from google import genai", source, notebook.name)

    def test_notebook_code_cells_compile_after_stripping_magics(self):
        for notebook in NOTEBOOKS:
            data = json.loads(notebook.read_text())
            for index, cell in enumerate(data.get("cells", [])):
                if cell.get("cell_type") != "code":
                    continue

                raw_source = "".join(cell.get("source", []))
                sanitized = "\n".join(
                    line for line in raw_source.splitlines() if not line.lstrip().startswith("!")
                )
                if not sanitized.strip():
                    continue

                compile(sanitized, f"{notebook.name}#cell{index}", "exec")


if __name__ == "__main__":
    unittest.main()
