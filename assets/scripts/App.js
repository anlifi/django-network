import React, { useState, useEffect } from 'react';
import ReactDOM from "react-dom";


const PostApp = function (props) {
  // Show loading screen till API data is fetched
  const [isLoading, setIsLoading] = useState(true);
  // State variable for list of posts
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Get posts from posts API
    fetch('/api/posts/')
      .then(res => res.json())
      .then((data) => {
        // Show posts
        console.log(data)
        setPosts(data);
        // Unset the "loading" flag
        setIsLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []); // Prevent continually hitting the APIs on state changes

  // Show a loading state if we haven't gotten data back yet
  if (isLoading) {
    return <p>Posts are loading...</p>;
  }
  // Show an "empty" state if we have no posts
  if (posts.length === 0) {
    return <p>No posts found!</p>;
  } else {
    // Show posts list component with the data we got back
    return <PostList posts={posts} />;
  }
}

const PostList = function (props) {
  // This component renders post containers
  return (
    <div>
      {
        props.posts.map((post, index) => {
          return (
            <div className="container-fluid border rounded-sm p-4" key={index}>
              <h4>{ post.username }</h4>
              <div className="container-fluid">
                <span className="row">{ post.content }</span>
                <small className="row text-muted">{ post.create_date }</small>
                <span id="post-likes" className="row">
                  <button id="btn-likes"><i className="fa fa-heart"></i></button>
                  { (post.likes.includes('None') ? 0 : post.likes ) }
                </span>
              </div>
            </div>
          );
        })
      }
    </div>
  );
};


export default PostApp;