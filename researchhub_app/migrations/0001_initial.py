# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Institution'
        db.create_table('researchhub_app_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('researchhub_app', ['Institution'])

        # Adding model 'SubjectProfile'
        db.create_table('researchhub_app_subjectprofile', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.IntegerField')()),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('researchhub_app', ['SubjectProfile'])

        # Adding model 'Study'
        db.create_table('researchhub_app_study', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('latest_birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('earliest_birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('contact_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['researchhub_app.Institution'])),
            ('irb_proposal', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('survey', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('irb_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('additional_criteria', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('researchhub_app', ['Study'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Institution'
        db.delete_table('researchhub_app_institution')

        # Deleting model 'SubjectProfile'
        db.delete_table('researchhub_app_subjectprofile')

        # Deleting model 'Study'
        db.delete_table('researchhub_app_study')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 29, 17, 26, 7, 703418, tzinfo=None)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 29, 17, 26, 7, 703310, tzinfo=None)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'researchhub_app.institution': {
            'Meta': {'object_name': 'Institution'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'researchhub_app.study': {
            'Meta': {'object_name': 'Study'},
            'additional_criteria': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'earliest_birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['researchhub_app.Institution']"}),
            'irb_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'irb_proposal': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'latest_birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'survey': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'researchhub_app.subjectprofile': {
            'Meta': {'object_name': 'SubjectProfile'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['researchhub_app']
