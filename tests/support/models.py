import time
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, JSON, String, Text

from tests.support.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    role = Column(String, default="pending")
    name = Column(String, nullable=True)


class File(Base):
    __tablename__ = "file"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    filename = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)
    meta = Column(JSON, nullable=True)
    hash = Column(Text, nullable=True)
    path = Column(Text, nullable=True)
    created_at = Column(BigInteger, default=lambda: int(time.time()))
    updated_at = Column(BigInteger, default=lambda: int(time.time()))


class Users:
    @staticmethod
    def get_users_by_user_ids(user_ids, db):
        if not user_ids:
            return []
        return db.query(User).filter(User.id.in_(user_ids)).all()


class Files:
    @staticmethod
    def get_file_by_id(file_id, db):
        return db.query(File).filter(File.id == file_id).first()

    @staticmethod
    def get_file_by_id_and_user_id(file_id, user_id, db):
        return (
            db.query(File)
            .filter(File.id == file_id, File.user_id == user_id)
            .first()
        )

    @staticmethod
    def update_file_data_by_id(file_id, data, db):
        db.query(File).filter(File.id == file_id).update(
            {"data": data, "updated_at": int(time.time())}
        )
        db.commit()

    @staticmethod
    def update_file_hash_by_id(file_id, file_hash, db):
        db.query(File).filter(File.id == file_id).update(
            {"hash": file_hash, "updated_at": int(time.time())}
        )
        db.commit()

    @staticmethod
    def update_file_by_id(id, form_data, db):
        updates = {}
        if hasattr(form_data, "hash") and form_data.hash is not None:
            updates["hash"] = form_data.hash
        if hasattr(form_data, "data") and form_data.data is not None:
            updates["data"] = form_data.data
        if hasattr(form_data, "meta") and form_data.meta is not None:
            updates["meta"] = form_data.meta
        updates["updated_at"] = int(time.time())

        db.query(File).filter(File.id == id).update(updates)
        db.commit()

    @staticmethod
    def update_file_metadata_by_id(file_id, metadata, db):
        file = db.query(File).filter(File.id == file_id).first()
        if file:
            if file.meta is None:
                file.meta = {}
            file.meta.update(metadata)
            file.updated_at = int(time.time())
            db.commit()
            db.refresh(file)
        return file

    @staticmethod
    def delete_file_by_id(file_id, db):
        db.query(File).filter(File.id == file_id).delete()
        db.commit()


class Groups:
    @staticmethod
    def get_groups_by_member_id(user_id, db):
        return []


class ModelForm(BaseModel):
    id: str
    name: Optional[str] = None
    base_model_id: Optional[str] = None
    meta: Optional[dict] = None
    params: Optional[dict] = None
    access_control: Optional[dict] = None
    is_active: Optional[bool] = None


class Models:
    @staticmethod
    def get_all_models(db):
        return []

    @staticmethod
    def update_model_by_id(model_id, model_form, db):
        return None
