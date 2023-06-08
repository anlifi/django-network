// import HTMX and inject it into the window scope
window.htmx = require('htmx.org');


window.addEventListener('DOMContentLoaded', () => {
  // Add event listeners to like btns for page posts on initial load
  updateLikes();
});


// Mutation Observer

// Select all nodes that will be observed for mutations (paginator buttons)
let targetNodes = document.querySelectorAll('.btn-page');

// Options for the observer (which mutations to observe)
const config = { attributes: true, subtree: true };

// Callback function to execute when mutations are observed
const callback = (mutationList, observer) => {
  for (const mutation of mutationList) {
    if (mutation.type === 'attributes') {
      // console.log(`The ${mutation.attributeName} attribute was modified.`);

      // Recursively observe newly loaded target nodes
      targetNodes = document.querySelectorAll('.btn-page');
      targetNodes.forEach(node => {
        observer.observe(node, config);
      })
      updateLikes();
    }
  }
};

// Create an observer instance linked to the callback function
const observer = new MutationObserver(callback);

// Start observing the target nodes for configured mutations
try {
  targetNodes.forEach(node => {
    observer.observe(node, config);
  });
}
catch {
  console.log("no nodes to observe");
}



// Helper functions

// Get like buttons and update likes when clicked
function updateLikes() {
  // Get all post like btns
  const likeBtns = document.querySelectorAll('.btn-likes');

  likeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Get post id from btn id and post likes element
      const postID = btn.id.split('-').pop();
      const postLikes = btn.nextElementSibling;

      // Send GET request to /like/<post_id> to update likes
      fetch(`/like/${postID}`)
        .then(res => res.json())
        .then(result => {
          result.user_liked ? btn.classList.add('liked') : btn.classList.remove('liked');
          postLikes.innerHTML = result.likes.length;
        })
    });
  });
}