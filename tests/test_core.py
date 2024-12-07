import os
import shutil
import pytest
from src.core import FileOrganizer

@pytest.fixture
def setup_environment(tmp_path):
    """Crea un entorno temporal para pruebas."""
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()
    return source, destination

def test_organize_file(setup_environment):
    source, destination = setup_environment
    file_path = source / "test.pdf"
    file_path.write_text("dummy content")

    organizer = FileOrganizer()
    organizer.rules = {"Documentos": [".pdf"]}
    result = organizer.organize_file(str(file_path), str(destination))

    assert result == "test.pdf -> Documentos"
    assert os.path.exists(destination / "Documentos" / "test.pdf")
