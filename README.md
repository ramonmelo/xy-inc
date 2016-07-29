# XY-Inc Test App
---
> This app is test program

## Usage

#### How prepare ?

1. Install `virtualenv` with: `sudo apt-get install virtualenv`
2. Create a virtual environment (_ve_) with: `virtualenv venv`
3. Initialize the _ve_ with: `source venv/bin/activate`
4. Install all dependencies with: `pip install -r requirements.txt`

> Every time to use the and run the code, execute the step **3** only.

#### How to run ?

```bash
python server.py # Will run the server on http://localhost:5000
```

> If the database file (`db.sqlite`) do not exist, it will be created at the first execution of the server.

#### Which request can I make ?

> **View Routes**

```bash
*[GET]* <HOST>/ # Redirect to create view
```

```bash
*[GET]* <HOST>/create/ # Shows a simple create form to insert POI on database
```

```bash
*[GET]* <HOST>/find/ # Shows a simple find view to list and filter POI
```

---
> **API Routes**

#### Request for creation of a new POI:

```bash
*[POST]* <HOST>/create_poi/
```

#### Parameters:
- **name** (string): The name of the POI
- **x** (int): The X position of the POI
- **y** (int): The Y position of the POI

#### Return (json):

```json
// If no error found
{
    "error": false,
    "msg": "Saved with success."
}
```
```
// If not all data was sent
{
    "error": true,
    "msg": "Please, send all data values."
}
```
```
// If the data was invalid
{
    "error": true,
    "msg": "Please, send valid values."
}
```

#### Request for list and filter POI:

```bash
*[GET]* <HOST>/list_poi/
```

#### Parameters:
- **x** (int): The X position of the base point
- **y** (int): The Y position of the base point
- **distance** (int): Max distance from base point to filter

#### Return (json):

```json
// If no error found
{
  "error": false,
  "msg": "",
  "result": [
    {
      "id": 1,
      "name": "Lanchonete",
      "x": 0,
      "y": 0
    },
    {
      "id": 2,
      "name": "Pub",
      "x": 2,
      "y": 3
    }
  ]
}
```
```json
// If no POI were registered or based on filters, all POI were filtered
{
  "error": true,
  "msg": "No results were found with current filters.",
  "result": []
}
```
