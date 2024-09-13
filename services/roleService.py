from models.role import Role
from database import db
from sqlalchemy import select,delete

def save(role_data):
    role_name = role_data.get('role_name')

    if not role_name:
        return {
            "status": "fail",
            "message": "Missing the required field,role name"
        }
    
    existing_role_query = select(Role).where(Role.role_name == role_name)
    existing_role = db.session.execute(existing_role_query).scalar_one_or_none()

    if existing_role:
        return{
            "status":"fail",
            "message":"Role table already has this role name entry"
        }
    try:
        new_role = Role(role_name = role_data["role_name"])

        db.session.add(new_role)
        db.session.commit()
        db.session.refresh(new_role)

        return{
            "status":"sucess",
            "message":"New Role successfully added",
            "data": new_role
        }
    
    except Exception as e:
        db.session.rollback()
        return{
            "status":"fail",
            "message": f"Failed to create new role:{str(e)}"
        }
    

def find_all():
    query = select(Role)
    all_roles = db.session.execute(query).scalars().all()
    return all_roles

def delete_role(id):
    query = select(Role).where(Role.id == id)
    role = db.session.execute(query).scalar()

    if role:
        db.session.delete(role)
        db.session.commit()
        return role
    else:
        return None
    
def update_role(id,data):
    try:
        query = select(Role).where(Role.id == id)
        role = db.session.execute(query).scalar()
        role.role_name = data.get("role_name",role.role_name)

        db.session.commit()
        return role
    except:
        return None
    




    
