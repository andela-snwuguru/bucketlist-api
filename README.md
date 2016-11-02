# bucketlist API
[![Build Status](https://travis-ci.org/andela-snwuguru/bucketlist-api.svg?branch=ch-ci-integration)](https://travis-ci.org/andela-snwuguru/bucketlist-api) [![Coverage Status](https://coveralls.io/repos/github/andela-snwuguru/bucketlist-api/badge.svg?branch=ch-ci-integration)](https://coveralls.io/github/andela-snwuguru/bucketlist-api?branch=ch-ci-integration)

According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.
This is a checkpoint 2 project used to evaluate Python beginner

## Features, Endpoints and Accessiblity
<table>
<tr>
<th> Features </th>
<th> Endpoint</th>
<th> Public</th>
</tr>
<tr>
 <td>Register </td>
 <td>POST /auth/register</td>
 <td> True</td>
</tr>
<tr>
<td>Authentication</td>
<td>POST /auth/login</td>
<td>True</td>
</tr>

<tr>
<td>Create Bucketlist</td>
<td>POST /bucketlists/ </td>
<td>False</td>
</tr>

<tr>
<td>Fetch Bucketlists</td>
<td>GET /bucketlists/ </td>
<td>False</td>
</tr>

<tr>
<td>Fetch Single Bucketlists</td>
<td>GET /bucketlists/:id </td>
<td>False</td>
</tr>

<tr>
<td>Update bucketlist record</td>
<td>PUT /bucketlists/:id </td>
<td>False</td>
</tr>

<tr>
<td>Delete bucketlist record</td>
<td>DELETE /bucketlists/:id </td>
<td>False</td>
</tr>

<tr>
<td>Create Bucketlist Item</td>
<td>POST /bucketlists/:id/items </td>
<td>False</td>
</tr>

<tr>
<td>Fetch Bucketlists Items</td>
<td>GET /bucketlists/:id/items </td>
<td>False</td>
</tr>

<tr>
<td>Fetch Single Bucketlists item</td>
<td>GET /bucketlists/:id/items/:itemId </td>
<td>False</td>
</tr>

<tr>
<td>Update bucketlist item record</td>
<td>PUT /bucketlists/:id/items/:itemId </td>
<td>False</td>
</tr>

<tr>
<td>Delete bucketlist item record</td>
<td>DELETE /bucketlists/:id/items/:itemId </td>
<td>False</td>
</tr>

</table>

## Dependecies
All dependecies can be found in requirements.txt

## How to use
- Clone project git clone `` git@github.com:andela-snwuguru/bucketlist-api.git ``
- Create a virtual environment `` mkvirtualenv bucketlist ``
- Install dependecies `` pip install -r requirements.txt ``
- Navigate to project folder `` cd ~/bucketlist-api ``
- Run migrationscript 
``` 
	python script.py db migrate 
	python script.py db upgrade 
```
- Run Project `` python run.py ``

## Sample Request

#### Register new User
```
Request
--------
http POST http://127.0.0.1:5000/api/v1.0/auth/register username=guru password=test email=guru@mail.com

Response
--------
{
  "data": {
    "date_created": "2016-05-19 19:37:20",
    "date_modified": "2016-05-19 19:37:20",
    "email": "guru@mail.com",
    "id": 7,
    "username": "guru"
  }
}
```

#### Retrieve Access Token
```
Request
--------
http POST http://127.0.0.1:5000/api/v1.0/auth/login username=guru password=test

Response
--------
{
  "data": {
    "date_created": "2016-05-19 19:37:20",
    "date_modified": "2016-05-19 19:37:20",
    "email": "guru@mail.com",
    "id": 7,
    "username": "guru"
  },
  "token": "098f6bcd4621d373cade4e832627b4f6|7|.Ch-n_A._bH9Hx_kpibiIlRHvFRZbVt-6UM"
}

```

### Documentation

Api documentation is still in progress, it Will soon be available.