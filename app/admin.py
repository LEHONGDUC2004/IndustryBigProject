from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, url_for, request, flash
from app.models import User, Project, Domain, Deployment, WebhookLog
from app.extensions import db

import hashlib
# --- Whitelist admin ---
ADMIN_EMAILS = {"admin@example.com"}
ADMIN_USERNAMES = {"admin"}

def is_admin_user(u):
    return bool(u) and ((u.email in ADMIN_EMAILS) or (u.name_account in ADMIN_USERNAMES))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not is_admin_user(current_user):
            return redirect(url_for('auth.admin_login', next=request.url))
        return super().index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and is_admin_user(current_user)
    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn cần đăng nhập bằng tài khoản admin.", "error")
        return redirect(url_for('auth.admin_login', next=request.url))


class UserAdmin(SecureModelView):
    column_list = ["id", "email", "name_account", "status"]
    column_searchable_list = ["email", "name_account"]
    column_filters = ["status"]
    column_labels = {
        "id": "Mã người dùng",
        "email": "Email",
        "name_account": "Tên tài khoản",
        "status": "Trạng thái",
    }
    form_excluded_columns = ["projects"]

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hashlib.md5(form.password.data.strip().encode("utf-8")).hexdigest()
        return super().on_model_change(form, model, is_created)

class ProjectAdmin(SecureModelView):
    column_list = ["id", "name", "account_id", "created_at"]
    column_filters = ["account_id", "created_at"]
    column_searchable_list = ["name"]
    column_labels = {
        "id": "Mã dự án",
        "name": "Tên dự án",
        "account_id": "Người dùng",
        "created_at": "Ngày tạo",
    }

class DomainAdmin(SecureModelView):
    column_list = ["id", "project_id", "domain", "verified"]
    column_filters = ["verified"]
    column_labels = {
        "id": "Mã domain",
        "project_id": "Dự án",
        "domain": "Domain",
        "verified": "Xác thực",
    }

class DeploymentAdmin(SecureModelView):
    column_list = ["id", "project_id", "status", "created_at"]
    column_filters = ["status", "created_at"]
    column_labels = {
        "id": "Mã deployment",
        "project_id": "Dự án",
        "status": "Trạng thái",
        "created_at": "Ngày tạo",
    }

class WebhookLogAdmin(SecureModelView):
    column_list = ["id", "project_id", "received_at"]
    column_labels = {
        "id": "Mã log",
        "project_id": "Dự án",
        "received_at": "Thời gian nhận",
    }

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('auth.admin_login'))
    def is_accessible(self):
        return current_user.is_authenticated

def init_admin(app):
    admin = Admin(app, name="IndustryProject Admin",
                  template_mode="bootstrap4",
                  index_view=MyAdminIndexView())
    admin.add_view(UserAdmin(User, db.session, name="Người dùng"))
    admin.add_view(ProjectAdmin(Project, db.session, name="Dự án"))
    admin.add_view(DomainAdmin(Domain, db.session, name="Domain"))
    admin.add_view(DeploymentAdmin(Deployment, db.session, name="Triển khai"))
    admin.add_view(WebhookLogAdmin(WebhookLog, db.session, name="Webhook Log"))
    admin.add_view(LogoutView(name="Đăng xuất"))
    return admin
