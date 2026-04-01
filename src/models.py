from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    phonenumber: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Usuarios que ME SIGUEN
    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.following_id",
        back_populates="following"
    )

    # Usuarios a los que YO SIGO
    followed: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active
        }


class Follower(db.Model):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    following_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    # Usuario seguido
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="followers"
    )

    # Usuario que sigue
    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followed"
    )
