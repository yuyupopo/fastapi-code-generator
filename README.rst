
fastapi-code-generator
======================

This code generator creates FastAPI app from an openapi file.


.. image:: https://badge.fury.io/py/fastapi-code-generator.svg
   :target: https://pypi.python.org/pypi/fastapi-code-generator
   :alt: PyPI version


.. image:: https://pepy.tech/badge/fastapi-code-generator/month
   :target: https://pepy.tech/project/fastapi-code-generator
   :alt: Downloads


.. image:: https://img.shields.io/pypi/pyversions/fastapi-code-generator
   :target: https://pypi.python.org/pypi/fastapi-code-generator
   :alt: PyPI - Python Version


.. image:: https://codecov.io/gh/koxudaxi/fastapi-code-generator/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/koxudaxi/fastapi-code-generator
   :alt: codecov


.. image:: https://img.shields.io/github/license/koxudaxi/fastapi-code-generator.svg
   :target: https://img.shields.io/github/license/koxudaxi/fastapi-code-generator.svg
   :alt: license


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black


This project is an experimental phase.
--------------------------------------

fastapi-code-generator uses `datamodel-code-generator <https://github.com/koxudaxi/datamodel-code-generator>`_ to generate pydantic models

Help
----

See `documentation <https://koxudaxi.github.io/fastapi-code-generator>`_ for more details.

Installation
------------

To install ``fastapi-code-generator``\ :

.. code-block:: sh

   $ pip install fastapi-code-generator

Usage
-----

The ``fastapi-code-generator`` command:

.. code-block::

   Usage: fastapi-codegen [OPTIONS]

   Options:
     -i, --input FILENAME     [required]
     -o, --output PATH        [required]
     -t, --template-dir PATH
     --install-completion     Install completion for the current shell.
     --show-completion        Show completion for the current shell, to copy it
                              or customize the installation.

     --help                   Show this message and exit.

Example
-------

OpenAPI
^^^^^^^

.. code-block:: sh

   $ fastapi-codegen --input api.yaml --output app


.. raw:: html

   <details>
   <summary>api.yaml</summary>
   <pre>
   <code>
   openapi: "3.0.0"
   info:
     version: 1.0.0
     title: Swagger Petstore
     license:
       name: MIT
   servers:
     - url: http://petstore.swagger.io/v1
   paths:
     /pets:
       get:
         summary: List all pets
         operationId: listPets
         tags:
           - pets
         parameters:
           - name: limit
             in: query
             description: How many items to return at one time (max 100)
             required: false
             schema:
               type: integer
               format: int32
         responses:
           '200':
             description: A paged array of pets
             headers:
               x-next:
                 description: A link to the next page of responses
                 schema:
                   type: string
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Pets"
           default:
             description: unexpected error
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Error"
                   x-amazon-apigateway-integration:
                     uri:
                       Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${PythonVersionFunction.Arn}/invocations
                     passthroughBehavior: when_no_templates
                     httpMethod: POST
                     type: aws_proxy
       post:
         summary: Create a pet
         operationId: createPets
         tags:
           - pets
         responses:
           '201':
             description: Null response
           default:
             description: unexpected error
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Error"
                   x-amazon-apigateway-integration:
                     uri:
                       Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${PythonVersionFunction.Arn}/invocations
                     passthroughBehavior: when_no_templates
                     httpMethod: POST
                     type: aws_proxy
     /pets/{petId}:
       get:
         summary: Info for a specific pet
         operationId: showPetById
         tags:
           - pets
         parameters:
           - name: petId
             in: path
             required: true
             description: The id of the pet to retrieve
             schema:
               type: string
         responses:
           '200':
             description: Expected response to a valid request
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Pets"
           default:
             description: unexpected error
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Error"
       x-amazon-apigateway-integration:
         uri:
           Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${PythonVersionFunction.Arn}/invocations
         passthroughBehavior: when_no_templates
         httpMethod: POST
         type: aws_proxy
   components:
     schemas:
       Pet:
         required:
           - id
           - name
         properties:
           id:
             type: integer
             format: int64
           name:
             type: string
           tag:
             type: string
       Pets:
         type: array
         description: list of pet
         items:
           $ref: "#/components/schemas/Pet"
       Error:
         required:
           - code
           - message
         properties:
           code:
             type: integer
             format: int32
           message:
             type: string
   </code>
   </pre>
   </details>


``app/main.py``\ :

.. code-block:: python

   # generated by fastapi-codegen:
   #   filename:  api.yaml
   #   timestamp: 2020-06-14T10:45:22+00:00

   from __future__ import annotations

   from typing import Optional

   from fastapi import FastAPI, Query

   from .models import Pets

   app = FastAPI(version="1.0.0", title="Swagger Petstore", license="{'name': 'MIT'}",)


   @app.get('/pets', response_model=Pets)
   def list_pets(limit: Optional[int] = None) -> Pets:
       """
       List all pets
       """
       pass


   @app.post('/pets', response_model=None)
   def create_pets() -> None:
       """
       Create a pet
       """
       pass


   @app.get('/pets/{pet_id}', response_model=Pets)
   def show_pet_by_id(pet_id: str = Query(..., alias='petId')) -> Pets:
       """
       Info for a specific pet
       """
       pass

``app/models.py``\ :

.. code-block:: python

   # generated by datamodel-codegen:
   #   filename:  api.yaml
   #   timestamp: 2020-06-14T10:45:22+00:00

   from typing import List, Optional

   from pydantic import BaseModel, Field


   class Pet(BaseModel):
       id: int
       name: str
       tag: Optional[str] = None


   class Pets(BaseModel):
       __root__: List[Pet] = Field(..., description='list of pet')


   class Error(BaseModel):
       code: int
       message: str

Custom Template
---------------

If you want to generate custom ``*.py`` files then you can give custom template directory fastapi-code-generator as ``-t`` or ``--template-dir`` options of the command.

fastapi-code-generator search `jinja2 <https://jinja.palletsprojects.com/>`_ template files in given template directory.

These files will be rendered and write to the output directory. Also, the generated file name will be created template file name which extension is replace to ``*.py``.

Variables
^^^^^^^^^

You can use below variables in jinja2 template


* ``imports``  all imports statements
* ``info``  all info statements
* ``operations`` ``operations`` is list of ``operation``

  * ``operation.type`` HTTP METHOD
  * ``operation.path`` Path
  * ``operation.snake_case_path`` Snake-cased Path
  * ``operation.response`` response object
  * ``operation.function_name`` function name is created ``operationId`` or ``METHOD`` + ``Path`` 
  * ``operation.snake_case_arguments`` Snake-cased function arguments
  * ``operation.security`` `Security <https://swagger.io/docs/specification/authentication/>`_
  * ``operation.summary`` a summary

default template
^^^^^^^^^^^^^^^^

``main.jinja2``

.. code-block:: jinja2

   from __future__ import annotations

   from fastapi import FastAPI

   {{imports}}

   app = FastAPI(
       {% if info %}
       {% for key,value in info.items() %}
       {{ key }} = "{{ value }}",
       {% endfor %}
       {% endif %}
       )


   {% for operation in operations %}
   @app.{{operation.type}}('{{operation.snake_case_path}}', response_model={{operation.response}})
   def {{operation.function_name}}({{operation.snake_case_arguments}}) -> {{operation.response}}:
       {%- if operation.summary %}
       """
       {{ operation.summary }}
       """
       {%- endif %}
       pass
   {% endfor %}

PyPi
----

`https://pypi.org/project/fastapi-code-generator <https://pypi.org/project/fastapi-code-generator>`_

License
-------

fastapi-code-generator is released under the MIT License. http://www.opensource.org/licenses/mit-license
