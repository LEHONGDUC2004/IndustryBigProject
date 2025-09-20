import os
from flask import Blueprint, render_template, redirect, request, url_for, flash, session, jsonify
from flask_login import login_required, logout_user, current_user
from app import login_manager, db
from app.controller.config import WEBHOOK_SECRET
main_bp = Blueprint('main', __name__)
from app.models import Deployment, WebhookLog, Project
login_manager.login_view = 'main.login'

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload_code')
def upload_code():
    return render_template('upload_code.html',name_user=current_user.name_account)

@main_bp.route('/deploy_code')
def deploy_code():
    return render_template('deploy.html',name_user=current_user.name_account)

@main_bp.route('/upload_infodb')
def upload_infodb():
    return render_template('upload/info_db.html',name_user=current_user.name_account)

@main_bp.route("/success")
@login_required
def success():
    jobs = session.get('jobs', [])
    return render_template("success.html", jobs=jobs,name_user=current_user.name_account)

@main_bp.route('/register')
def register():
    return render_template('register.html')



@main_bp.route('/verify')
def verify():
    return render_template('verify.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/indexLogin')
@login_required
def index_login():
    return render_template('indexLogin.html',name_user=current_user.name_account)

@main_bp.route('/logout')
def logout_process():
    return redirect(url_for('main.index'))

@main_bp.route('/passwd')
def setting_passwd():
    return render_template('setting/passwd.html',name_user=current_user.name_account)


@main_bp.route("/webhooks/jenkins", methods=["POST"])
def jenkins_webhook():
    if WEBHOOK_SECRET and request.headers.get("X-Webhook-Secret") != WEBHOOK_SECRET:
        return jsonify({"ok": False, "error": "forbidden"}), 403

    data = request.get_json(silent=True) or {}
    dep_id      = data.get("deploy_id") or data.get("DEPLOY_ID")
    status_raw  = (data.get("status") or "").upper()
    duration_ms = data.get("duration_ms") or 0
    job         = data.get("job")
    build_no    = data.get("build_number")
    build_url   = data.get("build_url")

    if dep_id:
        dep = Deployment.query.get(dep_id)
        if dep:
            # cập nhật trạng thái + thời gian
            if status_raw == "SUCCESS":
                dep.status = "success"
            elif status_raw == "FAILURE":
                dep.status = "failed"
            try:
                dep.build_time = float(duration_ms) / 1000.0
            except Exception:
                pass

            # append 1 dòng log ngắn
            summary = f"[{job}] #{build_no} {status_raw} {build_url or ''}".strip()
            dep.logs = (dep.logs or "")
            if summary and (not dep.logs or summary not in dep.logs):
                dep.logs += ("" if not dep.logs else "\n") + summary

            db.session.add(dep)
            db.session.add(WebhookLog(project_id=dep.project_id, payload=str(data)))
            db.session.commit()

    return jsonify({"ok": True})


@main_bp.get("/api/my_deployments")
@login_required
def api_my_deployments():
    project_id = request.args.get("project_id", type=int)
    limit = request.args.get("limit", default=50, type=int)

    q = (Deployment.query
         .join(Project, Deployment.project_id == Project.id)
         .filter(Project.account_id == current_user.id)
         .order_by(Deployment.created_at.desc()))
    if project_id:
        q = q.filter(Deployment.project_id == project_id)

    rows = q.limit(limit).all()
    # chèn tên project (nếu cần)
    for r in rows:
        _ = r.project
    return jsonify([
        {
            "id": d.id,
            "project_id": d.project_id,
            "project_name": d.project.name if d.project else None,
            "zip_filename": d.zip_filename,
            "status": d.status,
            "build_time": d.build_time,
            "created_at": d.created_at.isoformat() if d.created_at else None,
            "logs": d.logs or ""
        }
        for d in rows
    ])

