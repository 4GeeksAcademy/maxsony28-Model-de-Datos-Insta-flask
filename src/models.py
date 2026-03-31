from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    phonenumber: Mapped[str] = mapped_column(str(20))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    # birthday: Mapped[date] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


followers: Mapped[list["Follower"]] = relationship(
    "Follower",
    foreign_keys="Follower.user_id",
    back_populates="user"
)

# Usuarios a los que ESTE usuario sigue

followed: Mapped[list["Follower"]] = relationship(
    "Follower",
    foreign_keys="Follower.user_follower_id",
    back_populates="follower"
)


def serialize(self):
    return {
        "id": self.id,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        #   "birthday": self.birthday.isoformat(),
        "is_active": self.is_active
    }


class Follower(db.Model):
    __tablename__ = "followers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    user_follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    # Usuario seguido
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="followers"
    )

    # Usuario que sigue
    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_follower_id],
        back_populates="followed"
    )
