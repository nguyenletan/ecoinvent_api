from fastapi import FastAPI
import bw2data as bd
import bw2io as bi
from fastapi import Request

app = FastAPI()


@app.get("/")
async def root():
  return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
  return {"message": f"Hello {name}"}


@app.get("/search")
async def read_items(request: Request):
  search_string = request.query_params.get('search_string', None)
  print(search_string)
  # If you're just starting out, this should only have "default" in it.
  # Else, you'll see all the previous projects you've worked on.
  # You need to set a project. Give it a name!
  name = "bw25-tuto"
  bd.projects.set_current(name)

  # Import the path where your EI database is stored.
  # Note that the EI database must be unzipped and the path should end at the datasets folder.
  ei_path = "./ecoinvent_3.9.1_cutoff/datasets"

  # You will also need to give your database a name. This name will appear when you call bd.databases.
  # Here, I am using EI v3.9.1 cutoff.
  ei_name = "ecoinvent-391-cutoff"
  # %%
  # When we execute this cell, we will check if it's already been imported, and if not (else) we import it.
  result = ''
  if ei_name in bd.databases:
    result = "Database has already been imported."
    print("Database has already been imported.")
  else:
    result = "import Database"
    # Go ahead and import:
    ei_importer = bi.SingleOutputEcospold2Importer(ei_path, ei_name)
    # Apply strategies
    ei_importer.apply_strategies()
    # We can get some statistics
    ei_importer.statistics()
    # Now we will write the database into our project.
    ei_importer.write_database()

  eidb = bd.Database(ei_name)

  eidb.search(search_string)
  result = []
  for act in [act for act in eidb if search_string in act['name']]:
    # print(act.as_dict())
    result.append(act.as_dict())

  description = "The imported ecoinvent database is of type {} and has a length of {}.".format(type(eidb), len(eidb))
  return {
    "description": description,
    "result": result
  }
