import io
import tempfile
from typing import BinaryIO, Union, Optional
from utils.logger import log_error


class FileHelper:
    @staticmethod
    def get_file_content(file_path_or_content: Union[str, BinaryIO]) -> Optional[BinaryIO]:
        """Helper method to get file content from a path or BinaryIO."""
        if isinstance(file_path_or_content, str):
            try:
                with open(file_path_or_content, 'rb') as f:
                    return io.BytesIO(f.read())
            except IOError as e:
                log_error(f"Error opening file: {file_path_or_content}", str(e))
                return None
        else:
            file_path_or_content.seek(0)
            return file_path_or_content

    @staticmethod
    def create_temp_file(file_content: BinaryIO) -> str:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content.read())
            return temp_file.name