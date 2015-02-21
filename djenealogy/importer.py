from djenealogy.models import *
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class GedcomParser(object):
    
    def __init__(self, gedcom):
        """
        :param gedcom: a Gedcom model object
        """
        self.gedcom = gedcom
    
    @transaction.atomic
    def parse(self):
        """
        Parses a Gedcom object's attached file. Existing objects are removed
        from the database. Individuals and Familes are created, along with any
        attached Notes or Events. Works inside of an atomic transaction.
        """
        logger.info('Starting GEDCOM importer')
        self.clean()
        
        individuals = self.create_individuals()
        families = self.create_families()
        
        self.build_relationships(individuals, families)
        logger.info('Finished GEDCOM importer')


    def clean(self):
        """
        Cleans out existing records in the database attached to the Gedcom.
        """
        self.gedcom.individual_set.all().delete()
        logger.info('Deleted individuals')
        
        self.gedcom.family_set.all().delete()
        logger.info('Deleted families')
        
        self.gedcom.familyevent_set.all().delete()
        self.gedcom.individualevent_set.all().delete()
        logger.info('Deleted events')
        
        self.gedcom.note_set.all().delete()
        logger.info('Deleted notes')
    
    
    def create_individuals(self):
        """
        Loop through parsed Gedcom's individual list and create Individual
        objects. No families are attached at this stage. Notes and
        IndividualEvents are created and attached.
        
        :returns: list of created Individuals
        """
        logger.info('Creating individuals...')
        added = []
        
        for indv_ged in self.gedcom.parsed.individuals:
            # create basic individual and save
            indv_model = Individual.objects.create(
                gedcom = self.gedcom,
                xref = indv_ged.id,
                tag = indv_ged.tag,
                level = indv_ged.level,
                sex = indv_ged.sex,
                given_name = indv_ged.name[0],
                surname = indv_ged.name[1],
                prefix = indv_ged.title if indv_ged.title else ''
            )
            logger.debug('Created individual {0}'.format(indv_model))
            
            indv_model.notes.add(*self.create_notes(indv_ged))
            indv_model.save()
            
            self.create_individual_events(indv_ged, indv_model)
            
            added.append(indv_model)
            
        logger.info('Created {0} individuals'.format(len(added)))
        return added
    
    
    def create_families(self):
        """
        Loop through parsed Gedcom's families list and create Family objects.
        No children are added at this point. Notes and FamilyEvents are
        created and attached.
        
        :returns: list of created Families
        """
        added = []
        logger.info('Creating families...')
        
        for fam_ged in self.gedcom.parsed.families:
            fam_model = Family.objects.create(
                gedcom = self.gedcom,
                xref = fam_ged.id,
                tag = fam_ged.tag,
                level = fam_ged.level,
                value = fam_ged.value if fam_ged.value else ''
            )
            logger.debug('Created family {0}'.format(fam_model))
            
            self.create_family_events(fam_ged, fam_model)
            
            # find and attach husband and wife
            husbands = fam_ged.get_list('HUSB')
            if len(husbands):
                try:
                    i = Individual.objects.get(xref=husbands[0].value)
                except Individual.DoesNotExist:
                    logger.error('Could not find husband: {0]'.format(fam_ged))
                else:
                    fam_model.husband = i
                    logger.debug('Added husband {0} to family {1}'.format(i, fam_model))
            
            wives = fam_ged.get_list('WIFE')
            if len(wives):
                try:
                    i = Individual.objects.get(xref=wives[0].value)
                except Individual.DoesNotExist:
                    logger.error('Could not find wife: {0]'.format(fam_ged))
                else:
                    fam_model.wife = i
                    logger.debug('Added wife {0} to family {1}'.format(i, fam_model))
            
            fam_model.notes.add(*self.create_notes(fam_ged))
            
            fam_model.save()
            added.append(fam_model)
        
        logger.info('Created {0} families'.format(len(added)))
        return added
    
    
    def build_relationships(self, individuals, families):
        """
        Add children to Families. Lists of newly created individuals and
        families are used to prevent extra queries. This assumes the entire
        importing process is within a transaction. 
        
        :param individuals: a list of Individuals
        :param families: a list of Families
        """
        logger.info('Creating relationships...')
        
        for fam_ged in self.gedcom.parsed.families:
            # get cached family object
            fam_model = filter(lambda obj: obj.xref == fam_ged.id, families)
            if len(fam_model) != 1:
                logging.error('Could not find family: {0}'.format(fam_ged))
                continue
            fam_model = fam_model[0]
            
            # add children
            for child_ged in fam_ged.get_list('CHIL'):
                # get cached family object
                child_model = filter(lambda obj: obj.xref == child_ged.value, individuals)
                
                if len(child_model) != 1:
                    logging.error('Could not find individual: {0}'.format(child_ged))
                    continue
                child_model = child_model[0]
                
                fam_model.children.add(child_model)
                fam_model.save()
                logging.debug('Added child {0} to family {1}'.format(child_model, fam_model))
                
            fam_model.save()
            
    
    def create_individual_events(self, indv_ged, indv_model):
        """
        Creates and attaches any events found in an individual.
        
        :param indv_ged: an individual from a parsed Gedcom
        :param indv_model: an Individual model
        :returns: list of IndividualEvents
        """
        added = []
        
        for evt_type in IndividualEvent.TYPE_CHOICES:
            evts = indv_ged.get_list(evt_type[0])
            
            for evt_ged in evts:
                date = None
                try:
                    date = evt_ged['DATE'].value
                except IndexError:
                    pass
                
                place = None
                try:
                    place = evt_ged['PLAC'].value
                except IndexError:
                    pass
                
                evt, created = IndividualEvent.objects.get_or_create(
                    gedcom = self.gedcom,
                    individual = indv_model,
                    date = date,
                    place = place,
                    type = evt_ged.tag,
                    value = evt_ged.value,
                    level = evt_ged.level
                )
                logger.debug('Added individual event {0} to {1}'.format(evt, indv_model))
                
                evt.notes.add(*self.create_notes(evt_ged))
                evt.save()
                added.append(evt)
        
        return added
    
    
    def create_family_events(self, fam_ged, fam_model):
        """
        Creates and attaches any events found in a family.
        
        :param fam_ged: a family from a parsed Gedcom
        :param fam_model: a Family model
        :returns: list of FamilyEvents
        """
        added = []
        
        for evt_type in FamilyEvent.TYPE_CHOICES:
            evts = fam_ged.get_list(evt_type[0])
            
            for evt_ged in evts:
                date = None
                try:
                    date = evt_ged['DATE'].value
                except IndexError:
                    pass
                
                place = None
                try:
                    place = evt_ged['PLAC'].value
                except IndexError:
                    pass
            
                evt, created = FamilyEvent.objects.get_or_create(
                    gedcom = self.gedcom,
                    family = fam_model,
                    date = date,
                    place = place,
                    type = evt_ged.tag,
                    value = evt_ged.value,
                    level = evt_ged.level
                )
                logger.debug('Added family event {0} to {1}'.format(evt, fam_model))
                
                evt.notes.add(*self.create_notes(evt_ged))
                evt.save()
                added.append(evt)
        
        return added
        
            
    def create_notes(self, obj_ged):
        """
        Creates any notes found within the record of the parsed Gedcom.
        
        :param obj_ged: any record from a parsed Gedcom
        :returns: list of Notes
        """
        added = []
        notes = obj_ged.get_list('NOTE')
        
        for note in notes:
            try:
                note_ged = self.gedcom.parsed[note.value]
            except IndexError:
                pass
            else:
                if not note_ged.value:
                    note_ged.value = ''
                
                note_model, created = Note.objects.get_or_create(
                    gedcom = self.gedcom,
                    xref = note_ged.id,
                    tag = note_ged.tag,
                    level = note_ged.level,
                    full_text = note_ged.full_text
                )
                logger.debug('Added note {0}'.format(note_model))
                added.append(note_model)
        
        return added
    