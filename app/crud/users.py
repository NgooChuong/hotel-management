from sqlalchemy.orm import Session

from app.models.user import Users


class UserCRUD:
    def get_by_username(self, db: Session, username: str) -> Users | None:
        return db.query(Users).filter(Users.login == username).first()

    def create(self, db, username: str, password_hash: str):
        user = Users(login=username, password=password_hash, partner_id=1)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user_crud = UserCRUD()
