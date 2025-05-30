# BeBooked - A Social Media Platform For The Bookworms
#### Video Demo:  <https://www.youtube.com/watch?v=eCL5UM2o5Zg&t=8s&ab_channel=cs50finalproject>
#### Description:
This is a kind of social media that you post about books you read like what do you think about them what did you feel or what are their content what about their subject what do you suggest to new readers etc. You can post. You can write comment to your or other's posts. You can give `upvote` or `downvote` them. You can `follow` them and see their name on the right of the page and if you click on them you can access their profile page. Followers and Followings are counting on the profile page. You can change your profile settings by clicking the `Edit Profile` button and change things like `name`, `username`, `surname` and `biography`. Also you can change your password by clicking `change password` button
### Project File and Their Description:
## app.py
# Functions in app.py
**login_required**: Checks the if the user is logged in if not it directs user to login page
**index**: Renders the `index.html` template with `posts`, `user_id`, `username`, `currentusername` and `friends`
**filternovel**: Filters the `posts` to have only novel type books and renders the `index.html` template
**filterfiction**: Filters the `posts` to have only fiction type books and renders the `index.html` template
**filterstorybook**: Filters the `posts` to have only storybook type books and renders the `index.html` template
**filterhistory**: Filters the `posts` to have only history type books and renders the `index.html` template
**filterpoetry**: Filters the `posts` to have only poetry type books and renders the `index.html` template
**register**: Gets the username, name, surname, email, password, confirmation, country and birthday information from the `register.html` then checks is password and confirmation is same then checks does password have all the requirements that needed (minimum 8 characters, number, capital letters) if not refreshes the page and shows a flash message. Then checks is the username is different than the all the usernames in the database if not than create the account.
**login**: Gets the username/email and the password from the user and checks whether the user inputs an username or email it checks the database and checks if the passwords is correct if does than make user logged in.
**logout**: Make user logged out.
**post**: Gets the type of book, title, subject and content than create a new post into the posts section in the database.
**bigpost**: Gets the information of that post's id and the publisher's name then renders the `bigpost.html` with post's content, subject, upvote, downvote, comments, publisher's name , publisher's id, datetime information and the friend information of current user.
**findprofile**: renders the `profile.html` with all the information that a user could have.
**upvote**: makes the post upvoted and refreshes the main page.
**downvote**: makes the post downvoted and refreshes the main page.
**upvote2**: makes the post upvoted and refreshes the profile page.
**downvote2**: makes the post downvoted and refreshes the profile page.
**search**: gets the text from the searchbar and checks if it is empty or not. if it is empty than refreshes the main page if not takes the text and search in the usernames, subjects, titles and contents.
Than renders the `results.html` and show the search results. People can also be followed or unfollowed in there. Posts can also be clicked and opened in `bigpost.html` in there.
**editprofile**: Edit the profile settings like biography, name, surname, username. Gets the new information about the editable things and checks if the password is correct then edits. If the password is incorrect then refresh the page and shows a flash message that says the password is not correct.
**changepassword**: Checks if the current password is correct if it is than changes it to new password.
**addcomment**: Takes the comment text from the input box. Check if it is empty or not.If it is not empty then adds comment to the post which the user in.
**deletepost**: Deletes the post.
**deletecomment**: Deletes the comment.
**follow**: Follow the user.
**unfollow**: Unfollow the user.
## index.html
This is the main page. On the left there is filter section and filtering options. On the middle all the posts are here. On the right there is the followings section we can see and access the profiles of the people we follow.
## layout.html
This is the core of many html page. It has the upper part of the site such as main page button , searchbar and profile button.
## bigpost.html
This is the bigger page of the posts and there is a comment section downside. Filter and the followings section is also here too.
## login.html
Have two inputs username/email and password and have two buttons such as register and login. Login tries to log user in and register button directs user to register page.
## post.html
Have 3 text area and one selection for user the prepare his/her post. When clicked post button it creates the post.
## profile.html
Have the profile picture, nationality, age, birthday, biography, followers count and followings count on the upperside and also have the posts that user posted on the downside.
## register.html
Takes many inputs from the user then sends that infomation to the backend and creates the account.
## results.html
Has the results of the search on the middle. Filters on the left. Friends on the right.
