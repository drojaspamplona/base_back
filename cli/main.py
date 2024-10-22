import getopt
import os
import sys

import psycopg
from dotenv import dotenv_values
from jinja2 import Template
from psycopg.rows import dict_row


def validate_help(opts):
    if len([o for o in opts if "-h" in o or "--help" in o]) > 0:
        print("""
        -h or --help Pinta la ayuda
        -e or --entity El nombre de la entidad de base de datos
        -s or --schema El nombre del esquema que contiene la entidad de base de datos
        --no-repo Flag para indicar que no se debe crear un repositorio
        """)
        exit(0)


class Cli:
    def __init__(self):
        self.schema = ""
        self.entity = ""
        self.no_repo = False
        self.config = dotenv_values("../.env")
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_table_info(self):
        with psycopg.connect(host=self.config['DB_HOST'], user=self.config['DB_USER'],
                             password=self.config['DB_PASSWORD'], dbname=self.config['DB_DATABASE'],
                             row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select column_name, is_nullable,data_type
                from information_schema.columns
                where table_schema = %s and table_name = %s""", (self.schema, self.entity))
                return cur.fetchall()

    def build_model(self):
        table_info = self.get_table_info()
        columns, dependencies = self.parse_data_types(table_info)
        class_name = self.build_class_name()
        self.build_and_save_template("model", columns=columns, dependencies=dependencies,
                                     class_name=class_name)

    def build_service(self):
        class_name = self.build_class_name()
        self.build_and_save_template("service", class_name=class_name, schema=self.schema, entity=self.entity,
                                     no_repo=self.no_repo)

    def build_repository(self):
        if not self.no_repo:
            class_name = self.build_class_name()
            self.build_and_save_template("repository", class_name=class_name, schema=self.schema, entity=self.entity)

    def parse_data_types(self, table_info):
        optional_dependency = "from typing import Optional"
        dependencies = []
        for c in table_info:

            if c['is_nullable'] == 'YES' and optional_dependency not in dependencies:
                dependencies.append(optional_dependency)

            if c['data_type'] in ('money', 'real'):
                c['data_type'] = self.check_nullable(c, 'float')
            if c['data_type'] in ('integer', ''):
                c['data_type'] = self.check_nullable(c, 'int')
            if c['data_type'] in ('character varying', 'text'):
                c['data_type'] = self.check_nullable(c, 'str')
            if c['data_type'] in ('boolean', ''):
                c['data_type'] = self.check_nullable(c, 'bool')
            if c['data_type'] in ('timestamp without time zone', ''):
                c['data_type'] = self.check_nullable(c, 'datetime')
                dependencies.append("from datetime import datetime")
        return table_info, dependencies

    def build_class_name(self):
        words = self.entity.split("_")
        return "".join([w.title() for w in words])

    def build_and_save_template(self, template_name, **params):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates", f"{template_name}.txt")
        template = Template(open(path, "r").read())
        content = template.render(**params)
        self.save_file(template_name, content)

    def save_file(self, template_name, content):
        relative_path = self.get_relative_entity_path(template_name)
        self.create_schema_if_not_exist(relative_path)
        self.crate_or_edit_init(template_name, relative_path)
        path = os.path.join(self.base_path, relative_path, f"{self.entity}_{template_name}.py")
        f = open(path, "w+")
        f.write(content)
        f.close()

    def get_relative_entity_path(self, template_name):
        if template_name == "model":
            return os.path.join("domain", "models", self.schema)
        if template_name == "service":
            return os.path.join("domain", "services", self.schema)
        else:
            return os.path.join("repository", self.schema)

    def create_schema_if_not_exist(self, relative_path):
        full_path = os.path.join(self.base_path, relative_path)
        if not os.path.exists(full_path):
            os.mkdir(full_path)

    def crate_or_edit_init(self, template_name, relative_path):
        path = os.path.join(self.base_path, relative_path, "__init__.py")
        class_name = self.build_class_name()
        line = f"from .{self.entity}_{template_name} import {class_name}{template_name.title()}"
        f = open(path, "a+")
        f.write(f"{line}\n")
        f.close()

    @staticmethod
    def check_nullable(column, data_type):
        if column['is_nullable'] == 'YES':
            return f"Optional[{data_type}]"
        return data_type

    def main(self, argv):
        opts, args = getopt.getopt(argv, "hs:e:", ["help", "schema=", "entity=", "no-repo"])
        validate_help(opts)
        for opt, arg in opts:
            if opt == "--no-repo":
                self.no_repo = True
            if opt in ("-s", "--schema"):
                self.schema = arg
            if opt in ("-e", "--entity"):
                self.entity = arg

        self.build_model()
        self.build_service()
        self.build_repository()
        print("""
                    Please make sure to import the router into the init file and add the model properties
                """)


# def repository(self):
#     file_name, className = make_class_and_name("repository")
#     init = f"from .{file_name} import {className}"
#     check_or_create_schema(repositoryPath)
#     crate_or_edit_init(repositoryPath, init)
#     template = read_template("repository.txt")
#     content = template.render(className=className, id=name.capitalize(),
#                               schema=schema.capitalize(), name=name.capitalize())
#     save_template(repositoryPath, file_name, content)
#     return className
#
#
# def services(repositoryClassName, modelClassName):
#     fileName, className = make_class_and_name("service")
#     init = f"from .{fileName} import {className}"
#     check_or_create_schema(servicesPath)
#     crate_or_edit_init(servicesPath, init)
#     template = read_template("service.txt")
#     content = template.render(className=className,
#                               schema=schema, repositoryClassName=repositoryClassName,
#                               modelClassName=modelClassName)
#     save_template(servicesPath, fileName, content)
#     return className
#
#
# def model(self):
#     file_name, class_name = make_class_and_name("model")
#     init = f"from .{file_name} import *"
#     check_or_create_schema(modelPath)
#     crate_or_edit_init(modelPath, init)
#     template = read_template("model.txt")
#     content = template.render(className=class_name)
#     save_template(modelPath, file_name, content)
#     return class_name
#
#
# def api(model_class_name, service_class_name):
#     file_name, class_name = make_class_and_name("", True)
#     init = f"from .{file_name} import router as {file_name}Router"
#     check_or_create_schema(apiPath)
#     crate_or_edit_init(apiPath, init)
#     template = read_template("api.txt")
#     content = template.render(modelClassName=model_class_name, name=name.lower(),
#                               schema=schema, serviceClassName=service_class_name)
#     save_template(apiPath, file_name, content)
#
#
# def check_or_create_schema(relative_path):
#     full_path = f"{path}{relative_path}{schema}"
#     if not os.path.exists(full_path):
#         os.mkdir(full_path)
#
#
# def read_template(name) -> Template:
#     f = open(f"./templates/{name}", "r")
#     return Template(f.read())
#
#
# def save_template(relative_path, file_name, contect: str):
#     f = open(f"{path}{relative_path}{schema}/{file_name}.py", "w+")
#     f.write(contect)
#     f.close()
#
#
# def crate_or_edit_init(relativePath, line):
#     f = open(f"{path}{relativePath}{schema}/__init__.py", "a+")
#     f.write(f"{line}\n")
#     f.close()
#
#
# def make_class_and_name(suffix: str, api=False):
#     file_name = name[0].lower() + name[1:]
#     file_name = f"{file_name}_{suffix}"
#     class_name = name + suffix.capitalize()
#     if api:
#         return name[0].lower() + name[1:], class_name
#     return file_name, class_name


if __name__ == "__main__":
    Cli().main(sys.argv[1:])
