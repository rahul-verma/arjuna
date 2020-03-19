#### Concise Basic Interactions with a Gui Element - You Can Write Concise Code If You Wish

Code style could be a very personal thing. If you are looking for a concise coding option, you can write the previous code as follows with exact same functionality:

#### The Test Fixture

We use the same test fixture code as from the previous example.

#### The GNS File

We use the same GNS file `WordPress.yaml` from previous example.

### Usage

```python
# arjuna-samples/arjex/test/module/check_07_basicinteract_refined.py

@test
def check_wp_login_concise(request, wordpress):
    
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    wordpress.gns.user.text = user
    wordpress.gns.pwd.text = pwd
    wordpress.gns.submit.click()
    wordpress.gns.view_site

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)
    wordpress.gns.logout_confirm.click()
    wordpress.gns.logout_msg
```
