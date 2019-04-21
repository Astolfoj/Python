# -*- coding: utf-8
import os
import time 
import datetime as t 
import json
archivo = "contactos.json"
'''
Diccionario de contacto
=======================

data = {
        contactos: [
                      {
                      'nombre': None,
                      'apellido': None,
                      'telefono': {
                                  'fijo': None,
                                  'movil': None,
                                  },
                      'email': {
                                'personal': None,
                                'trabajo': None, 
                               }
                      'fecha_nac': None,
                     },
                ]
       }
'''

class _Contacto:
    def __init__(self, nombre = '', apellido = '', telefono_fijo = '', telefono_movil = '', 
                 email_personal = '' ,email_trabajo = '', fecha_nac = '', edad = ''):
        self.nombre = nombre.capitalize()
        self.apellido = apellido.capitalize()
        self.telefono_fijo = telefono_fijo
        self.telefono_movil = telefono_movil
        self.email_personal = email_personal
        self.email_trabajo = email_trabajo
        self.fecha_nac = fecha_nac
        self.__edad = self.__set_edad(self.fecha_nac) 
        
    def __set_edad(self,fecha_nac):
        #Se crea una variable con el tiempo actual
        if fecha_nac != "":
            Actual = t.datetime.now()
        
        #Se separa el str de la fecha de nacimiento en otra variable"
            lis_fech = fecha_nac.split('/')
        
        #La variable se almacena con la fecha actual
            usuario_fecha = t.datetime(int(lis_fech[2]),int(lis_fech[1]),int(lis_fech[0]))
        
        #Se restan ambas y se crea una cantidad de dias
            nueva_fecha = Actual - usuario_fecha
        
        #Se retorna la cantidad de dias 
            return str(nueva_fecha.days //365)
        else:
            return ""
    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, val):
        self.__nombre = val
     
    
    @property
    def apellido(self):
        return self.__apellido
    
    @apellido.setter
    def apellido(self, val):
        self.__apellido = val

    
    @property
    def telefono_fijo(self):
        return self.__telefono_fijo
    
    @telefono_fijo.setter
    def telefono_fijo(self, val):
        self.__telefono_fijo = val

    
    @property
    def telefono_movil(self):
        return self.__telefono_movil
    
    @telefono_movil.setter
    def telefono_movil(self, val):
        self.__telefono_movil = val
        
    @property
    def email_personal(self):
        return self.__email_personal
    
    @email_personal.setter
    def email_personal(self, val):
        self.__email_personal = val

    @property
    def email_trabajo(self):
        return self.__email_trabajo
    
    @email_trabajo.setter
    def email_trabajo(self, val):
        self.__email_trabajo = val

    @property
    def edad(self):
        return self.__edad
            
    def __repr__(self):
        
        str_out = "Contacto:\n"
        str_out += "\tNombre: {}\n".format(self.nombre)
        str_out += "\tApellido: {}\n".format(self.apellido)
        str_out += "\tTelefonos: \n"
        str_out += '\t\tFijo: {}\n'.format(self.telefono_fijo)
        str_out += '\t\tMovil: {}\n'.format(self.telefono_movil)
        str_out += "\tEmail: \n"
        str_out += '\t\tTrabajo: {}\n'.format(self.email_trabajo)
        str_out += '\t\tPersonal: {}\n'.format(self.email_personal)
        str_out += "\tFecha de Nacimiento: {}\n".format(self.fecha_nac)
        str_out += "\tEdad: {}\n".format(self.edad)
        return str_out
    

def clear_screen():
    _ = os.system('cls')
    return None


def show_menu():
    clear_screen()
    print("\nAGENDA DE CONTACTOS")
    print("====================")
    print("[1] Mostrar contactos")
    print("[2] Ver detalle de contactos")
    print("[3] Editar contacto")
    print("[4] Borrar contacto")
    print("[5] Agregar contacto")
    print("[0] Salir")
    opc = int(input("\nOpcion: "))
    
    return opc


def read_file(file):
    '''
    Esta funcion lee un archivo json con la informacion de los contactos
    registrados y retorna una lista con objetos Contacto
    '''
    with open(file) as f:
        lista_dic = json.load(f)['contactos']
        lista_contactos = []
        for contacto in lista_dic:
            lista_contactos.append(_Contacto(contacto["nombre"],contacto["apellido"],contacto["telefono"]["fijo"],contacto["telefono"]["movil"],
                                            contacto["email"]["personal"],contacto["email"]["trabajo"], contacto["fecha_nac"]))
        return lista_contactos
            


def write_file(file, contact_list): 
    '''
    Esta funcion crear un diccionario con la informacion de la lista de 
    contactos (con objetos Contacto) y escribe un archivo json con la
    informacion del diccionario
    '''
    with open(file , mode = 'w') as f:
        lista_dic = []
        for contacto in contact_list:
            lista_dic.append({'nombre':contacto.nombre,'apellido':contacto.apellido,
                  'telefono':{'fijo':contacto.telefono_fijo,'movil':contacto.telefono_movil},
                  'email':{'personal':contacto.email_personal,'trabajo':contacto.email_trabajo},
                  "fecha_nac":contacto.fecha_nac})
        dic_contactos = {'contactos':lista_dic}
        json.dump(dict(dic_contactos),f)



def find_contact(contact_list):
    '''
    Esta funcion busca en una lista de contactos (con objetos Contactos)
    un contacto especificado por nombre
    '''
    name_str = input("Ingrese el nombre del contacto: ")
    for contacto in contact_list:
        nombre_comp = contacto.nombre + ' ' + contacto.apellido
        if name_str.lower() in nombre_comp.lower():
            return contacto
    else:
        print("El contacto ingresado no existe")


def edit_contact(contact_list):
    '''
    Funcion que cambia los cambios de un objeto Contacto
    '''
    contacto = find_contact(contact_list)
    informacion_contacto = {'nombre':contacto.nombre,'apellido':contacto.apellido,
                  'telefono':{'fijo':contacto.telefono_fijo,'movil':contacto.telefono_movil},
                  'email':{'personal':contacto.email_personal,'trabajo':contacto.email_trabajo},
                  "fecha_nac":contacto.fecha_nac}
    for propiedad,valor in zip(informacion_contacto.keys(),informacion_contacto.values()):
        if not isinstance(valor, dict):
            nuevo = input(f"{propiedad.capitalize()}[{valor}]: ")
            if nuevo != "":
                informacion_contacto[propiedad]=nuevo
            else:
                informacion_contacto[propiedad]=valor
        else:
            print(propiedad.capitalize())
            diccionario = valor
            for propiedad,valor in zip(diccionario.keys(),diccionario.values()):
                nuevo = input(f"{propiedad.capitalize()}[{valor}]: ")
                if nuevo != "":
                    diccionario[propiedad]=nuevo
                else:
                    diccionario[propiedad]=valor
            
    contact_list.remove(contacto)
    contacto = _Contacto(informacion_contacto["nombre"],informacion_contacto["apellido"],informacion_contacto["telefono"]["fijo"],
               informacion_contacto["telefono"]["movil"],informacion_contacto["email"]["personal"],informacion_contacto["email"]["trabajo"],
               informacion_contacto["fecha_nac"])
    contact_list.append(contacto)
    input("Contacto editado exitosamente!")
    return contact_list
    
def add_contact(contact_list):
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    telefono_fijo = input("Telefono fijo: ")
    telefono_movil = input("Telefono movil: ")
    email_personal = input("Email personal: ")
    email_trabajo = input("Email trabajo: ")
    fecha_nac = input("Fecha de nacimiento: ")
    contact_list.append(_Contacto(nombre,apellido,telefono_fijo, telefono_movil, email_personal, email_trabajo,
                                 fecha_nac))
    input("Contacto agregado exitosamente!")
    return contact_list

def delete_contact(contact_list):
    '''
    Funcion que elimina un objeto Contacto de una lista de objetos Contactos
    '''
    contacto = find_contact(contact_list)
    contact_list.remove(contacto)
    input("Contacto eliminado exitosamente!")
    return contact_list


def show_contact(contact_list):
    '''
    Funcion que muestra los detalles de un objeto Contacto <print(obj)>
    '''
    contacto = find_contact(contact_list)
    print(contacto)


def list_contact(contact_list):
    '''
    Funcion que muestra un listado de contactos numerados con la informacion
    de nombre y apellido en ordenado de forma alfabetica
    '''
    contact_list.sort(key=lambda x: x.nombre[0])
    i=1
    print("Contactos: ")
    for contacto in contact_list:
        print(f"\t{i:3} - {contacto.nombre} {contacto.apellido}")
        i+=1


def salir():
    '''
    Funcion que pide al usuario confirmacion para salir. Retorrna un boolean.
    '''
    y_n = input("\nSeguro desea salir? [Si/No]: ")
    
    if y_n[0].upper() == "S":
        return True
    else:
        return False

def main():
    lista_contactos = read_file(archivo)
    while True:
        opc = show_menu()
        if opc is 1:
            clear_screen()
            list_contact(lista_contactos)
            input("\nPresiona 'Enter' para volver al menu")
            
        elif opc == 2:
            clear_screen()
            show_contact(lista_contactos)
            input("\nPresiona 'Enter' para volver al menu")
        
        elif opc == 3:
            clear_screen()
            lista_contactos = edit_contact(lista_contactos)
            
        elif opc == 4:
            clear_screen()
            lista_contactos = delete_contact(lista_contactos)
        
        elif opc == 5:
            clear_screen()
            lista_contactos = add_contact(lista_contactos)
            
        
        elif opc == 0:
            if salir():
                write_file(archivo,lista_contactos)
                break
                
        else:
            print("\nLa opcion ingresada no es valida")


if __name__ == '__main__':
    main()