from sqlalchemy import Boolean, Column, ForeignKey, Integer,BigInteger, String,TIMESTAMP,ForeignKeyConstraint,text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "auth_user"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), unique=True, index=True,nullable=False)
    password = Column(String(255),nullable=False)
    name = Column(String(300),nullable=False)
    email = Column(String(255))
    is_active = Column(Boolean, default=False,nullable=False,server_default=text('0'))
    is_superuser = Column(Boolean, default=False,nullable=False,server_default=text('0'))
    date_joined = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
    )
    
class Group(Base):
    __tablename__ = "auth_group"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(150),nullable=False)
    
    permissions = relationship("Permission", secondary="auth_group_has_permission", back_populates='auth_permission')
    
class PermissionModel(Base):
    __tablename__ = "auth_permission_model"
    
    id = Column(Integer, primary_key=True)
    model = Column(String(100),nullable=False)
    name = Column(String(150),nullable=False)
    description = Column(String(300),nullable=False)
    
    permissions = relationship("Permission", back_populates="auth_permission")
    
class Permission(Base):
    __tablename__ = "auth_permission"
    
    model_id = Column(Integer, ForeignKey("auth_permission_model.id"),primary_key=True)
    code = Column(String(100),primary_key=True)
    name = Column(String(255),nullable=False)
    
    model = relationship("PermissionModel", back_populates="auth_permission_model")
    groups = relationship("Group", secondary="auth_group_has_permission", back_populates='auth_group')
    
class GroupPermission(Base):
    __tablename__ = "auth_group_has_permission"

    group_id = Column(Integer, ForeignKey('auth_group.id',ondelete='CASCADE'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('auth_permission.id',ondelete='CASCADE'), primary_key=True)
    
class UserGroup(Base):
    __tablename__ = "auth_user_has_group"

    user_id = Column(Integer, ForeignKey('auth_user.id',ondelete='CASCADE'), primary_key=True)
    group_id = Column(Integer, ForeignKey('auth_group.id',ondelete='CASCADE'), primary_key=True)