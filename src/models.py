from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime

db = SQLAlchemy()

# Tabla User


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    birthday: Mapped[date] = mapped_column()
    phonenumber: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    # Followers
    followers: Mapped[list["Follower"]] = relationship(
        back_populates="following",
        foreign_keys="Follower.following_id"
    )

    following: Mapped[list["Follower"]] = relationship(
        back_populates="follower",
        foreign_keys="Follower.follower_id"
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    post_likes: Mapped[list["PostLike"]] = relationship()
    comment_likes: Mapped[list["CommentLike"]] = relationship()


def serialize(self):
    return {
        "id": self.id,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "birthday": self.birthday.isoformat() if self.birthday else None,
        "phonenumber": self.phonenumber,
        "is_active": self.is_active,
        "followers_count": len(self.followers),
        "following_count": len(self.following)
    }


# Seguidores Follower


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
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    follower: Mapped["User"] = relationship(
        foreign_keys=[follower_id],
        back_populates="following"
    )
    following: Mapped["User"] = relationship(
        foreign_keys=[following_id],
        back_populates="followers"
    )


def serialize(self):
    return {
        "follower_id": self.follower_id,
        "following_id": self.following_id,
        "created_at": self.created_at.isoformat()
    }


# Post

class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_text: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    media: Mapped[list["Media"]] = relationship(back_populates="post")
    likes: Mapped[list["PostLike"]] = relationship(back_populates="post")


def serialize(self):
    return {
        "id": self.id,
        "post_text": self.post_text,
        "user_id": self.user_id,
        "likes_count": len(self.likes),
        "comments_count": len(self.comments),
        "media_count": len(self.media)
    }


# Comentarios de los usuari@


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship(back_populates="comments")
    likes: Mapped[list["CommentLike"]] = relationship(back_populates="comment")


def serialize(self):
    return {
        "id": self.id,
        "comment_text": self.comment_text,
        "user_id": self.user_id,
        "post_id": self.post_id,
        "likes_count": len(self.likes)
    }

# Media


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20))  # image | video
    url: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post: Mapped["Post"] = relationship(back_populates="media")

# Tabla para postear PostLike


class PostLike(db.Model):
    __tablename__ = "post_likes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship(back_populates="likes")


def serialize(self):
    return {
        "user_id": self.user_id,
        "post_id": self.post_id,
        "created_at": self.created_at.isoformat()
    }

# Clase para la estructura de la tabla CommentLike


class CommentLike(db.Model):
    __tablename__ = "comment_likes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id"),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship()
    comment: Mapped["Comment"] = relationship(back_populates="likes")


def serialize(self):
    return {
        "user_id": self.user_id,
        "comment_id": self.comment_id,
        "created_at": self.created_at.isoformat()
    }
