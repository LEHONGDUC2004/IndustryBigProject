from datetime import datetime
from flask_login import UserMixin
from app.extensions import db



# Tài khoản người dùng
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name_account = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=True)

    # Một tài khoản có nhiều project
    projects = db.relationship('Project', backref='account', lazy=True)

    def __repr__(self):
        return f"<Account {self.name_account}>"


# Dự án được triển khai
class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name_sql = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name_host = db.Column(db.Text, nullable=False)
    name_user = db.Column(db.Text, nullable=False)
    name_database = db.Column(db.Text, nullable=False)
    passwd = db.Column(db.Text, nullable=False)
    # Quan hệ 1:N
    deployments = db.relationship('Deployment', backref='project', lazy=True)
    webhook_logs = db.relationship('WebhookLog', backref='project', lazy=True)
    domains = db.relationship('Domain', backref='project', lazy=True)

# Lần triển khai cụ thể của project
class Deployment(db.Model):
    __tablename__ = 'deployment'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    zip_filename = db.Column(db.String(255))
    status = db.Column(db.String(50), default='pending')
    logs = db.Column(db.Text)
    build_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Lưu log của các webhook
class WebhookLog(db.Model):
    __tablename__ = 'webhook_log'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    payload = db.Column(db.Text)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

# Domain custom
class Domain(db.Model):
    __tablename__ = 'domain'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    domain = db.Column(db.String(255), unique=True)
    verified = db.Column(db.Boolean, default=False)
