import uuid
import hashlib

def generate_user_id() -> str:
    """
    Genera un ID de usuario anónimo único (UUID4).
    """
    return str(uuid.uuid4())

def generate_user_hash(user_id: str, secret_phrase: str) -> str:
    """
    Genera un hash SHA-256 a partir del user_id y la palabra secreta del usuario.
    Este hash representa su identidad anónima validable.
    """
    raw_string = f"{user_id}:{secret_phrase}"
    return hashlib.sha256(raw_string.encode()).hexdigest()

def validate_user_hash(user_id: str, secret_phrase: str, submitted_hash: str) -> bool:
    """
    Valida si el hash entregado por el usuario coincide con el generado desde su user_id y palabra secreta.
    """
    expected_hash = generate_user_hash(user_id, secret_phrase)
    return expected_hash == submitted_hash
