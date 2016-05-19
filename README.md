# bucketlist API
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
- Clone project git clone git@github.com:andela-snwuguru/bucketlist-api.git
- Create a virtual environment `` mkvirtualenv bucketlist ``
- Install dependecies `` pip install -r requirements.txt ``
- Navigate to project folder `` cd ~/bucketlist-api ``
- Run migrationscript 
``` 
	python script.py db makemigrations
	python script.py db migrate 
	python script.py db upgrade 
```
- Run Project `` python run.py ``
