from neo4j_for_django.db.base import gdbh
from neo4j_for_django.db.exceptions import *
import re


class DatabaseNode:
    """
    This class has tools to :
    - Transform Python objects like lists and dictionaries in a Cypher format : format_labels_to_cypher(),
      format_properties_to_cypher().
    - Create a node in the database : create()

    :param (optional) labels : a list of all the node's labels. No labels = None. Default = None
    :param (optional) properties_fields : a dictionary of all the node's properties, where keys are the names of the properties and values their
      values. No properties = None. Default = None
    :param (optional) properties_items_dict:

    """

    def __init__(self, labels=None, properties_fields=None, properties_items_dict=None):
        self.labels = labels
        self.properties_fields = properties_fields
        self.properties_items_dict = properties_items_dict
        self.create()

    def create(self):
        """
        This method handle datas' formatting to cypher language, and the node's creation in the database.
        :return: It return the create node.
        """
        object_labels = self._format_labels_to_cypher()
        object_properties = self._format_properties_to_cypher()

        response = gdbh.w_transaction('CREATE (n:%s %s) RETURN (n)' % (object_labels, object_properties))

    def _format_labels_to_cypher(self):
        """
        This method converts labels list format in a cypher labels format.

        :return: Cypher formatted labels.
        """
        render = []

        if isinstance(self.labels, list):
            for label in self.labels:
                render.append(label)
            return ':'.join(render)

        else:
            raise N4DNodeLabelsInitializationError('self.labels attribute must be a list.')

    # Convert dict format to a cypher properties format
    def _format_properties_to_cypher(self):
        """
        This method converts properties dict format in a cypher properties format.

        :return: Cypher formatted properties.
        """

        if self.properties_fields is None or not self.properties_fields:    # SEE TO DELETE 'is None' part (cause we receive an empty dict, and an empty dict is not None)
            return '{}'  # That's an empty cypher properties container

        else:
            if isinstance(self.properties_items_dict, dict):
                render = []

                for field_name, field_value in self.properties_fields.items():
                    for key, value in self.properties_items_dict.items():
                        if field_value.key == key:

                            if isinstance(value, int) or isinstance(value, bool):
                                render.append(key + ': ' + str(value))

                            else:
                                value_render = '"' + str(value) + '"'
                                render.append(key + ': ' + value_render)

                return '{' + ', '.join(render) + '}'

            else:
                raise N4DNodeLabelsInitializationError("'self.properties_value' attribute must be a dict.")


class Property:
    """
    This class can be directly instantiate, but could be also overridden to create specific properties.

    :param (required) key: The key is the the name of the property. The key will be used to access to a object property content
                (object.key) but also to do researches into the Neo4j database.
    :param (optional) content: The content is the value of a property.
    :param (optional) required: If set on True, and if the content of the property is empty, an error will be raised.
    :param (optional) required: If set on True, and if the content of the property combinaison key+content is already
                                in the database, an error will be raised.
    :param (optional) default: A default value that will fill the content if is empty.



    """

    def __init__(self, key=None, content=None, required=False, unique=False, default=None):
        self.key = key
        self.content = content
        self.required = required
        self.unique = unique
        self.default = default


    @staticmethod
    def _build(node_object, recovered_fields_values):
        """
        This method take a Node object and datas recovered during its instantiation and _build a dictionary that contains
        key+content combinations for each property of the object.
        :param node_object: An instance of the Node class.
        :param recovered_fields_values: The dictionary of values recovered during the instantiation of the Node class
                                        or one of these children.
        :return: A dictionary that contains key+content combinations for the given object.
                 NB : All property without content nor 'default' parameter, will be filled by 'None'.
        """
        properties_items_dict = {}
        # All the attributes (representing the properties of the Node) of the current node class.
        properties_fields = node_object.__class__._get_properties_fields().items()

        # List that contains keys-values tuple of the parameters of the instance (a = SomeClass(key=value, key...)
        not_defined_fields = [field_item for field_item in properties_fields]

        for field_name, field_content in properties_fields:
            if field_content._check_property_datas(node_object, recovered_fields_values):

                for key, value in recovered_fields_values.items():
                    if value is not None:

                        # Check properties initial fields and recovered properties datas during instanciation
                        if ('_' + key) == field_name:
                            not_defined_fields.remove((field_name, field_content))
                            if callable(value):
                                callable_result = value()

                                setattr(node_object, key, callable_result)
                                properties_items_dict[key] = callable_result

                            else:
                                setattr(node_object, key, value)
                                properties_items_dict[key] = value

        # Treat the undefined fields
        for field_item in not_defined_fields:
            if field_item[1].default is not None:
                if callable(field_item[1].default):
                    callable_result = field_item[1].default()

                    setattr(node_object, field_item[1].key, callable_result)
                    properties_items_dict[field_item[1].key] = callable_result

                else:
                    setattr(node_object, field_item[1].key, field_item[1].default)
                    properties_items_dict[field_item[1].key] = field_item[1].default

            else:
                setattr(node_object, field_item[1].key, None)
                properties_items_dict[field_item[1].key] = None

        return properties_items_dict

    def _check_property_datas(self, node_object, property_recovered_datas):
        """
        This method checks and enforces the restrictions (required, unique, etc...) of a field.

        :param node_object: An instance of the Node class.
        :param property_recovered_datas: The dictionary of values recovered during the instantiation of the Node class
                                         or one of these children.

        :return:
        """
        property_field_name = self.key

        try:
            property_associate_datas = property_recovered_datas[property_field_name]

        except KeyError:
            # Check if a property is 'required' :
            if self.required and self.default is None:
                raise N4DRequiredConstraintError(f"An instance of {node_object.__class__.__name__} must have a '{property_field_name}'.")

        else:
            # Check if a property is 'unique' :
            if self.unique:
                # Try to get an instance of the current node class with the same property
                if isinstance(property_associate_datas, str):
                    query = 'MATCH (n:%s) WHERE n.%s = "%s" RETURN (n)' % (node_object.labels, property_field_name, property_associate_datas)
                    result = gdbh.r_transaction(query)

                else:
                    query = 'MATCH (n:%s) WHERE n.%s = %s RETURN (n)' % (node_object.labels, property_field_name, property_associate_datas)
                    result = gdbh.r_transaction(query)

                # If an instance is found, raise an error
                if result:
                    raise N4DUniqueConstraintError(f"An instance of {node_object.__class__.__name__} must have an UNIQUE '{property_field_name}'.")
                else:
                    return True
            else:
                return True

        finally:
            # Checks if a property is not be at the same time 'required' and with a 'default' value :
            if self.required and self.default is not None:
                raise N4DAttributeError('A field must not have "required=True" and a "default" value.')


class Node:
    """
    This is the base class for all Node classes.
    """
    def __init__(self, **received_properties_dict):
        self.current_object_properties_dict = None
        self._constructor(received_properties_dict)

    def _constructor(self, received_properties_dict):
        """
        This method handle the construction of a node, it ensures a creation in the database and as a python instance.
        :param received_properties_dict: The dictionary of values recovered during the instantiation of the Node class
                                         or one of these children.
        """
        self.current_object_properties_dict = Property._build(self, received_properties_dict)
        DatabaseNode(labels=self.__class__.get_labels(), properties_fields=self.__class__._get_properties_fields(),
                     properties_items_dict=self.current_object_properties_dict)

    @classmethod
    def get_labels(cls):
        """
        This method detects and regroups in a list, all labels of a Node instance. Then, it returns the list.
        :return: A list of all Node instance's labels.
        """
        labels_list = []
        class_dict = cls.__dict__.items()

        for key, value in class_dict:
            if str(key) == 'labels':
                if isinstance(value, list):
                    for label in value:
                        labels_list.append(label)

                elif isinstance(value, str):
                    labels_list.append(value)
        if not cls.__name__ in labels_list:
            labels_list.append(cls.__name__)

        return labels_list

    def get_properties(self):
        return self.current_object_properties_dict

    @classmethod
    def _get_properties_fields(cls):
        """
        This method detects and regroups in a dictionary, all properties of a Node instance. Then, it returns the
        dictionary.
        :return: A dictionary of all Node instance's properties.
        """
        properties_dict = {}
        class_dict = cls.__dict__.items()

        for k, v in class_dict:
            if not re.match('^(<function|<classmethod|<class|<__main__|<staticmethod)', str(v)):
                if not (k.startswith('__') and k.endswith('__')) and k.startswith('_'):
                    properties_dict[k] = v

            # Support for local test with "if __name__ == '__main__': etc... "
            elif str(v).startswith('<__main__'):
                if not str(k) == 'labels':
                    properties_dict[k] = v

        return properties_dict



