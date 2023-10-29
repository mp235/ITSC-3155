from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import models


def create(db: Session, resource):
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )

    db.add(db_resource)
    # Commit the changes to the database
    db.commit()
    # Refresh the Resource object to ensure it reflects the current state in the database
    db.refresh(db_resource)
    # Return the newly created Sandwich object
    return db_resource


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()


def update(db: Session, resource_id: int, resource):
    # Query the database for the specific Resource to update
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Extract the update data from the provided 'Resource' object
    update_data = resource.dict(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_resource.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated Resource record
    return db_resource.first()


def delete(db: Session, resource_id: int):
    # Query the database for the specific Resource to delete
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Delete the database record without synchronizing the session
    db_resource.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
