from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from app import db
import uuid

class Utility(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

# Model to deploy
class Track(db.Model,Utility):
    __metaclass__=Utility()
    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    filename = db.Column(db.Text, nullable=True)
    hash = db.Column(db.Text, nullable=True)
    uploaded_on = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    track_report = relationship("Ioc_Report", backref="track")
    
    def add_analyzed_file(filename,hash):
        Track(filename=filename,hash=hash).save()
    
    def delete_file(id):
        Track.query.filter(Track.id == id).delete()
        db.session.commit()
        
    def report_exists(hash):
        return bool(Track.query.filter(Track.hash == hash).first() is not None )
    
    def get_report_name(hash):
        return Track.query.filter_by(hash=hash).first().filename
    
    def get_report_id_by_hash(hash):
        return Track.query.filter_by(hash=hash).first().id
 
    def get_report_id_by_name(filename):
        return Track.query.filter_by(filename=filename).first().id    
    
class Ioc_Report(db.Model,Utility):
    __metaclass__=Utility()
    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    iocs = db.Column(db.JSON, nullable=True)
    pages = db.Column(db.JSON, nullable=True)
    file_metadata = db.Column(db.JSON, nullable=True)
    track_id = db.Column(db.Text(length=36), ForeignKey("track.id"))
    
    def save_iocs(iocs,pages,file_metadata,track_id):
        Ioc_Report(iocs=iocs,pages=pages,file_metadata=file_metadata,track_id=track_id).save()
    
    def get_iocs_by_id(report_id):
        return [Ioc_Report.query.filter_by(track_id=report_id).first().iocs,Ioc_Report.query.filter_by(track_id=report_id).first().pages,Ioc_Report.query.filter_by(track_id=report_id).first().file_metadata]