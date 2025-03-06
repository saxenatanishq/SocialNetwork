addEventListener("DOMContentLoaded",() => {
    document.addEventListener('click', event => {
        const element1 = event.target;
        if (element1.parentElement.className === "like_button"){
            id1 = element1.parentElement.parentElement.parentElement.id
            fetch(`/thread/${id1}`, {
                method: "PUT"
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector(`#like_count_${id1}`).innerHTML = data.like_count;
                if (data.liked){
                    document.querySelector(`#like_button_${id1}`).innerHTML = '<img src="/static/network/dislike.png" alt="like" id="like_pic">';
                }else{
                    document.querySelector(`#like_button_${id1}`).innerHTML = '<img src="/static/network/like.png" alt="like" id="like_pic">';
                }
            })
            .catch(error => console.error("Error liking thread:", error))
        } else if (element1.className === "follow_button") {
            let id1 = element1.id.split("_")[1];
            fetch(`/user_api/${id1}`, {
                method: "PUT"
            })
            .then(response => response.json())
            .then(data => {
                if (data.following){
                    document.querySelector(`#button_${id1}`).innerHTML = "Unfollow";
                }else{
                    document.querySelector(`#button_${id1}`).innerHTML = "Follow";
                }  
                document.querySelector("#followers_count").innerHTML = "Followers : " + data.follower_count;
            })
            .catch(error => console.error("Error in (un)following a user"));
        } else if (element1.classList.contains("edit_button")) {
            id1 = element1.id.split("_")[1];
            element1.style.display = "none";
            document.querySelector(`#thread_body_${id1}`).style.display = "none";
            document.querySelector(`#hidden_thread_part_${id1}`).style.display = "block";
        } else if (element1.classList.contains("thread_edit_submit_button")) {
            id1 = element1.id.split("_")[1];
            let new_content = document.querySelector(`#thread_textarea_${id1}`).value;
            console.log(new_content)
            fetch(`edit_api/${id1}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: new_content })
            })
            .catch(error => console.error("Error in editing the thread"));
            document.querySelector(`#hidden_thread_part_${id1}`).style.display = "none";
            document.querySelector(`#thread_body_${id1}`).innerHTML = new_content;
            document.querySelector(`#thread_body_${id1}`).style.display = "block";
            document.querySelector(`#edit_${id1}`).style.display = "block";
        }
    });
});