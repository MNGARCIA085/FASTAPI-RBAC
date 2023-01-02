from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from databases.config import get_db
from .. import models,schemas
import functools

""" 1. GET """





#
def get_groups(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    return db.query(models.Groups).offset(skip).limit(limit).all()


""" 2. POST """


def post_group(group: schemas.Group, db: Session = Depends(get_db)):
    db_item = models.Groups(**group.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item




""" 3. GET by id """
def get_group_by_id(group_id:int,db: Session = Depends(get_db)):
    group = db.query(models.Groups).filter(models.Groups.id==group_id).first()
    if group:
        return group
    raise HTTPException(status_code=404, detail="Department not found")




""" 4. UPDATE """

def update_group(group_id: int, group: schemas.Group, db: Session = Depends(get_db)):
    db_group = db.query(models.Groups).filter(models.Groups.id == group_id).first()
    if db_group:
        for var, value in vars(group).items():
            setattr(db_group, var, value) if value else None
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group
    else:
        raise HTTPException(status_code=400, detail="Department with id %s not found" % group_id)



""" 5. DELETE """
def delete_group(group_id,db: Session = Depends(get_db)):
    try:
        aux = db.query(models.Groups).filter_by(id=group_id).delete()
        if aux == 0:
            raise HTTPException(status_code=400, detail="Department with id %s not found" % group_id)
        else:
            db.commit()
        return {'Msg':"Department with id %s deleted" % group_id}
    except HTTPException as e:
        raise
    except Exception as e:
        #print(e); esto no va para el usuario sino para mi login
        raise HTTPException(status_code=500, detail="Server Error")
    return






"""
# mapeo de nombres y claves; tmb. podría definir consultas del tipo FK
def mapeo():
    return {
        "tipo": models.Sede.tipo,
        "direccion": models.Sede.direccion,
        "nombre": models.Sede.nombre,
    }


def filter_department(data):
    queries = [models.Sede.id > 0]
    campos = mapeo()
    for clave, valor in data.items():
        if valor:
            if isinstance(valor, str):
                queries.append(campos[clave] == valor)
            elif isinstance(valor, list):
                queries_aux = []
                for v in valor:
                    queries_aux.append(campos[clave] == v)
                query_aux = functools.reduce(lambda a, b: a | b, queries_aux)
                queries.append(query_aux)
    query = functools.reduce(lambda a, b: (a & b), queries)
    return query



uso:

query = filter_department(
        {
            'tipo': tipo,
            'direccion': direccion,
            'nombre': nombre
        })
    return list(db.query(models.Sede).filter(query).offset(skip).limit(limit))

"""