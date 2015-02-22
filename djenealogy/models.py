from django.db import models
import codecs
from dateutil.parser import parse as parse_date

'''
TODO

Source
Repository
Submisison
Address?

'''



''' Abstract models '''
class TimestampBase(models.Model):
    class Meta:
        abstract = True
    
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class RecordBase(models.Model):
    """
    Represents a common GEDCOM record.
    """
    class Meta:
        abstract = True
    
    gedcom = models.ForeignKey('Gedcom')
    xref = models.CharField(max_length=15)
    tag = models.CharField(max_length=127)
    value = models.CharField(max_length=255, null=True, blank=True)
    level = models.IntegerField()


class NoteBase(models.Model):
    class Meta:
        abstract = True
    
    notes = models.ManyToManyField('Note', blank=True, null=True)


class Event(TimestampBase, NoteBase):
    class Meta:
        abstract = True
    
    gedcom = models.ForeignKey('Gedcom')
    value = models.CharField(max_length=255, null=True, blank=True)
    level = models.IntegerField()
    place = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=32, null=True, blank=True)
    
    @property
    def date_parsed(self):
        if not self.date:
            return None
            
        try:
            dt = parse_date(self.date)
        except ValueError:
            return None
        
        return dt




''' Object models '''
class Gedcom(TimestampBase):
    __original_file = None
    __api = None
    
    file = models.FileField(upload_to='gedcoms')
    name = models.CharField(max_length=127)
    slug = models.SlugField(unique=True)
    
    def __init__(self, *args, **kwargs):
        super(Gedcom, self).__init__(*args, **kwargs)
        self.__original_File = self.file
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # test if the file has been changed
        updated_file = self.file != self.__original_file
        
        # save to database
        super(Gedcom, self).save(force_insert, force_update, *args, **kwargs)
        
        # if file was updated and the parsed gedcom is exists, update
        if updated_file and self.__api is not None:
            self.__update_api()
        
        self.__original_file = self.file
    
    def __update_api(self):
        """
        Updates the underlying parsed object if a file is set.
        """
        if self.file:
            import gedcom as G
            self.__api = G.parse(codecs.open(self.file.path, 'r', 'utf-8'))
    
    @property
    def parsed(self):
        """
        Access the parsed gedcom object.
        
        :returns: gedcom instance, from gedcompy
        """
        if not self.__api:
            self.__update_api()
        return self.__api


    def __unicode__(self):
        """
        :rtype: str
        """
        return u'{0}'.format(self.name)


class Note(TimestampBase, RecordBase):
    full_text = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'{0}'.format(self.full_text[:25])


class Individual(TimestampBase, RecordBase, NoteBase):
    '''
    TODO
    
    OCCU occupation
    CAST caste
    DESR description
    EDUC education
    ALIA alias 
    DESI / ANSI
    INDO
    NATI
    PROP
    RELI
    RESI
    SSN
    '''
    
    class Meta:
        ordering = ('surname', 'given_name', 'nickname',)
        unique_together = ('gedcom', 'xref',)
        
    SEX_CHOICES = (
        ('U', 'Unknown'),
        ('M', 'Male'),
        ('F', 'Female')
    )
    
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=SEX_CHOICES[0])
    relate1 = models.PositiveIntegerField(blank=True, null=True)
    relate2 = models.PositiveIntegerField(blank=True, null=True)
    surname = models.CharField(max_length=127, blank=True)
    given_name = models.CharField(max_length=127, blank=True)
    prefix = models.CharField(max_length=127, blank=True)
    suffix = models.CharField(max_length=127, blank=True)
    nickname = models.CharField(max_length=127, blank=True)
    birth_year = models.PositiveSmallIntegerField(blank=True, null=True)
    death_year = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'{0} {1}'.format(self.given_name, self.surname).strip()

    @property
    def birth(self):
        """
        Gets the first found birth event.
        
        :returns: IndividualEvent
        """
        return self.events.filter(type='BIRT').first()
    
    @property
    def death(self):
        """
        Gets the first found death event.
        
        :returns: IndividualEvent
        """
        return self.events.filter(type='DEAT').first()

    @property
    def father(self):
        """
        Gets the husband from the first found parent family.
        
        :returns: Individual or None
        """
        family = self.parent_families.exclude(husband__isnull=True).first()
        if family:
            return family.husband
        return None
    
    @property
    def mother(self):
        """
        Gets the wife from the first found parent family.
        
        :returns: Individual or None
        """
        family = self.parent_families.exclude(wife__isnull=True).first()
        if family:
            return family.wife
        return None
    
    @property
    def parents(self):
        """
        Returns all husbands and wives in the parent families.
        
        :returns: list of Individuals
        """
        parents = []
        for p in self.parent_families.all():
            parents += [self.father, self.mother]
        return parents
    
    def is_parent(self, individual):
        """
        Tests if the given individual is a parent of this individual by
        searching through parent_families.
        
        :param individual: Individual
        :rtype: boolean
        """
        return self.parent_families.filter(models.Q(husband=individual) | models.Q(wife=individual)).count() > 0
    
    @property
    def siblings(self):
        """
        Returns individuals that belong in the current individual's parent
        families.
        
        :returns: Individual QuerySet
        """
        return Individual.objects.exclude(id=self.id).filter(parent_families__in=self.parent_families.all()).distinct()
    
    def is_sibling(self, individual):
        """
        Tests if the given individual exists in the siblings list.
        
        :param individual: Individual
        :rtype: boolean
        """
        return self.siblings.filter(id=individual.id).count() > 0
   
    @property
    def families(self):
        """
        Returns all families where this individual is either a husband or a wife.
        
        :returns: Family QuerySet
        """
        if self.sex == 'M':
            return self.husband_roles
        elif self.sex == 'F':
            return self.wife_roles
            
        return Family.objects.none()
    
    @property
    def spouses(self):
        """
        Returns all individuals that are partners of self appearing in a
        wife or husband role.
        
        :returns: Individual Queryset
        """
        if self.sex == 'M':
            return Individual.objects.filter(wife_roles__husband=self)
        elif self.sex == 'F':
            return Individual.objects.filter(husband_roles__wife=self)
        
        return Individual.objects.none()

    @property
    def children(self):
        """
        Returns all children where this individual is either a husband or wife
        in the parent families.
        
        :returns: Individual QuerySet
        """
        if self.sex == 'M':
            return Individual.objects.filter(parent_families__husband=self)
        elif self.sex == 'F':
            return Individual.objects.filter(parent_families__wife=self)
            
        return Individual.objects.none()
    
    def mutual_families(self, relative):
        """
        Checks my parent_families and returns any families that are also
        parent_families of the given individual.
        
        TODO test this
        Source: dijxtra/simplepyged
        
        :param relative: Individual
        :returns: list of Families
        """
        mutual = []
        for my_family in self.parent_families.all():
            if relative.parent_families.filter(xref=my_family.xref).exists():
                mutual.append(my_family)
        return mutual
    
    def common_ancestor(self, relative):
        """
        Gets the common ancestor between me and a known relative.
        
        TODO test this
        Source: dijxtra/simplepyged
        
        :param relative: Individual
        :returns: Individual or None
        """
        if relative is None:
            return None
        
        me = {}
        him = {}
        
        me['new'] = [self]
        me['old'] = []
        him['new'] = [relative]
        him['old'] = []
        
        while(me['new'] != [] or him['new'] != []):
            for p in me['new']:
                if p in him['new']:
                    return p
            
            for p in me['new']:
                if p in him['old']:
                    return p
                
            for p in him['new']:
                if p in me['old']:
                    return p
            
            for l in [me, him]:
                new = []
                for p in l['new']:
                    new.extend(p.parents)
                new = filter(lambda x: x is not None, new)
                l['old'].extend(l['new'])
                l['new'] = new
            
        return None
    
    def is_relative(self, individual):
        """
        Tests if the given individual has a common ancestor.
        
        TODO test this
        Source: dijxtra/simplepyged
        
        :param individual: Individual
        :rtype: boolean
        """
        return self.common_ancestor(individual) is not None
    
    
    def distance_to_ancestor(self, ancestor):
        """
        Calculates the distance between me and a known ancestor.
        
        TODO test this
        Source: dijxtra/simplepyged
        
        :param ancestor: Individual
        :rtype: int or None
        """
        distance = 0
        ancestor_list = [self]
        
        while ancestor_list != []:
            if ancestor in ancestor_list:
                return distance
            
            new_list = []
            for a in ancestor_list:
                new_list.extend(a.parents)
                if None in new_list:
                    new_list.remove(None)
                
            ancestor_list = new_list
            distance += 1
        
        return None

    @staticmethod
    def down_path(ancestor, descendant, distance=None):
        """
        Finds the path between an ancestor and a descendant.
        
        TODO test this
        Source: dijxtra/simplepyged
        
        :param ancestor: Individual
        :param descendant: Individual
        :param distance: int or None
        :returns: None or list of Individuals
        """
        if distance is not None:
            if distance <= 0:
                return None
        
        if ancestor.children == []:
            return None
        
        if descendant in ancestor.children:
            return [ancestor]
        
        for c in ancestor.children:
            if distance is None:
                path = ancestor.down_path(c, descendant)
            else:
                path = ancestor.down_path(c, descendant, distance-1)
            
            if path is not None:
                path.insert(0, ancestor)
                return path
        
        return None

    def path_to_relative(self, relative):
        """
        Gets the path to a relative by finding a common ancestor and traversing
        the down_path between the common ancestor.
        
        :param relative: an Individual
        :returns: list of [Individual, 'relationship']
        """
        if relative == self: return []
        
        if relative in self.parents:
            return [[self, 'start'], [relative, 'parent']]
        
        common_ancestor = self.common_ancestor(relative)
        
        if common_ancestor is None:
            return None
        
        if common_ancestor == self:
            my_path = []
        else:
            my_path = self.down_path(common_ancestor, self, self.distance_to_ancestor(common_ancestor))
        
        if common_ancestor == relative:
            his_path = []
        else:
            his_path = self.down_path(common_ancestor, relative, relative.distance_to_ancestor(common_ancestor))
        
        my_path.append(self)
        his_path.append(relative)
        
        my_path.reverse()
        
        full_path = []
        for step in my_path[:-1]:
            full_path.append([step, 'parent'])
        
        try:
            if full_path[-1][0].is_sibling(his_path[1]):
                full_path[-1][1] = 'sibling'
            else:
                full_path.append([common_ancestor, 'child'])
        except IndexError:
            full_path.append([common_ancestor, 'child'])
        
        for step in his_path[1:]:
            full_path.append([step, 'child'])
        full_path[-1][1] = ''
        
        return full_path


class Family(TimestampBase, RecordBase, NoteBase):
    class Meta:
        ordering = ('husband__surname', 'husband__given_name', 'wife__surname', 'wife__given_name',)
        unique_together = ('gedcom', 'xref', 'husband', 'wife',)
        verbose_name_plural = 'families'
    
    husband = models.ForeignKey('Individual', related_name='husband_roles', blank=True, null=True)
    wife = models.ForeignKey('Individual', related_name='wife_roles', blank=True, null=True)
    children = models.ManyToManyField('Individual', related_name='parent_families', blank=True, null=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.husband, self.wife).strip()
    
    @property
    def is_married(self):
        """
        Returns status if husband and wife have marriage events.
        
        :rtype: boolean
        """
        return self.events.filter(type='MARR').count() > 0
        
    def is_relative(self, individual):
        """
        Tests if the individual is related to this Family by checking if they
        are related to either the husband or the wife.
        
        :param individual: Individual
        :rtype: boolean
        """
        if self.huband and self.husband.is_relative(individual): return True
        if self.wife and self.wife.is_relative(individual): return True
        
        return False


class IndividualEvent(Event):
    TYPE_CHOICES = (
        ('EVEN', 'General event'),
        ('BIRT', 'Birth'),
        ('CHR', 'Christening'),
        ('DEAT', 'Death'),
        ('BURI', 'Burial'),
        ('CREM', 'Cremation'),
        ('ADOP', 'Adoption'),
        ('BAPM', 'Baptism'),
        ('BARM', 'Bar Mitzvah'),
        ('BASM', 'Bas Mitzvah'),
        ('BLES', 'Blessing'),
        ('CHRA', 'Adult christening'),
        ('CONF', 'Confirmation'),
        ('FCOM', 'First communion'),
        ('ORDN', 'Ordination'),
        ('NATU', 'Naturalization'),
        ('EMIG', 'Emigration'),
        ('IMMI', 'Immigration'),
        ('CENS', 'Census'),
        ('PROB', 'Property'),
        ('WILL', 'Will'),
        ('GRAD', 'Graduation'),
        ('RETI', 'Retirement'),
    )
    
    individual = models.ForeignKey('Individual', related_name='events')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=TYPE_CHOICES[0])

    def __unicode__(self):
        return u'{0} - {1}'.format(self.get_type_display(), self.individual)


# TODO fix unicode()s to reduce queries
class FamilyEvent(Event):
    TYPE_CHOICES = (
        ('EVEN', 'General event'),
        ('ANUL', 'Annulment'),
        ('CENS', 'Census'),
        ('DIV', 'Divorce'),
        ('DIVF', 'Divorce filed'),
        ('ENGA', 'Engagement'),
        ('MARR', 'Marriage'),
        ('MARB', 'Marriage bann'),
        ('MARC', 'Marriage contract'),
        ('MARL', 'Marriage license'),
        ('MARS', 'Marriage settlement'),
    )
    
    family = models.ForeignKey('Family', related_name='events')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=TYPE_CHOICES[0])

    def __unicode__(self):
        return u'{0} - {1}'.format(self.get_type_display(), self.family)
