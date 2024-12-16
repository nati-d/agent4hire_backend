import praw
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditClient:
    def __init__(self):
        
        
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")
        username = os.getenv("REDDIT_USERNAME")
        password = os.getenv("REDDIT_PASSWORD")
      
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password
            )
        except Exception as e:
            logger.error(f"Failed to authenticate with Reddit API: {e}")

    def get_info(self, ids):
        """
        Fetch detailed information on specific posts or comments.
        :param ids: List of fullnames (e.g., 't3_postid', 't1_commentid')
        :return: Information on posts/comments or error message
        """
        try:
            info = list(self.reddit.info(ids))
            logger.info(f"Retrieved information for IDs: {ids}")
            return info
        except Exception as e:
            logger.error(f"Error fetching information for IDs {ids}: {e}")
            return {"error": str(e)}

    def vote(self, thing_id, direction):
        """
        Vote on a post or comment.
        :param thing_id: Fullname of the item to vote on (e.g., 't3_postid')
        :param direction: 1 for upvote, -1 for downvote, 0 to remove vote
        :return: Success or error message
        """
        try:
            submission = self.reddit.submission(id=thing_id.split('_')[1])
            submission.vote(direction)
            logger.info(f"Voted on {thing_id} with direction {direction}")
        except Exception as e:
            logger.error(f"Error voting on {thing_id}: {e}")
            return {"error": str(e)}

    def submit_post(self, subreddit, title, selftext=""):
        """
        Submit a new post to a subreddit.
        :param subreddit: The subreddit to post to
        :param title: Title of the post
        :param selftext: Text content of the post
        :return: Submission object or error message
        """
        try:
            submission = self.reddit.subreddit(subreddit).submit(title=title, selftext=selftext)
            logger.info(f"Submitted post to r/{subreddit} with title '{title}'")
            return submission
        except Exception as e:
            logger.error(f"Error submitting post to r/{subreddit}: {e}")
            return {"error": str(e)}

    def search_subreddits(self, query):
        """
        Search for subreddits matching a query.
        :param query: Search query
        :return: List of subreddit objects or error message
        """
        try:
            subreddits = list(self.reddit.subreddits.search(query))
            logger.info(f"Found {len(subreddits)} subreddits for query '{query}'")
            return subreddits
        except Exception as e:
            logger.error(f"Error searching subreddits for query '{query}': {e}")
            return {"error": str(e)}

    def get_new_posts(self, subreddit, limit=5):
        """
        Retrieve the latest posts from a subreddit.
        :param subreddit: Subreddit name
        :param limit: Number of posts to retrieve
        :return: List of submission objects or error message
        """
        try:
            new_posts = list(self.reddit.subreddit(subreddit).new(limit=limit))
            logger.info(f"Retrieved {len(new_posts)} new posts from r/{subreddit}")
            return new_posts
        except Exception as e:
            logger.error(f"Error fetching new posts from r/{subreddit}: {e}")
            return {"error": str(e)}

    def get_subreddit_info(self, subreddit):
        """
        Retrieve details about a specific subreddit.
        :param subreddit: Subreddit name
        :return: Subreddit object or error message
        """
        try:
            subreddit_info = self.reddit.subreddit(subreddit)
            logger.info(f"Retrieved info for subreddit r/{subreddit}")
            return subreddit_info
        except Exception as e:
            logger.error(f"Error retrieving subreddit info for r/{subreddit}: {e}")
            return {"error": str(e)}
        
    def search_content(self, query, subreddit=None, limit=10):
        """
        Search for content across Reddit or within a specific subreddit.
        :param query: Search query
        :param subreddit: Subreddit to search within (optional)
        :param limit: Number of search results to return
        :return: List of submission objects or error message
        """
        try:
            if subreddit:
                search_results = list(self.reddit.subreddit(subreddit).search(query, limit=limit))
                logger.info(f"Found {len(search_results)} results in r/{subreddit} for query '{query}'")
            else:
                search_results = list(self.reddit.subreddit('all').search(query, limit=limit))
                logger.info(f"Found {len(search_results)} results across Reddit for query '{query}'")
            return search_results
        except Exception as e:
            logger.error(f"Error searching content for query '{query}': {e}")
            return {"error": str(e)}

    def get_user_overview(self, username, limit=10):
        """
        Retrieve an overview of a user's activity (posts and comments).
        :param username: Reddit username to fetch activity for
        :param limit: Number of activities to return
        :return: List of submission/comment objects or error message
        """
        try:
            user = self.reddit.redditor(username)
            user_overview = list(user.submissions.new(limit=limit)) + list(user.comments.new(limit=limit))
            logger.info(f"Retrieved overview of user '{username}' with {len(user_overview)} activities")
            return user_overview
        except Exception as e:
            logger.error(f"Error retrieving user overview for '{username}': {e}")
            return {"error": str(e)}
        
    def send_private_message(self, recipient, subject, message):
        """
        Send a private message to a Reddit user.
        :param recipient: Username of the recipient
        :param subject: Subject of the message
        :param message: Body of the message
        :return: Success or error message
        """
        try:
            self.reddit.redditor(recipient).message(subject, message)
            logger.info(f"Sent private message to {recipient} with subject '{subject}'")
            return {"status": "Message sent"}
        except Exception as e:
            logger.error(f"Error sending message to {recipient}: {e}")
            return {"error": str(e)}

    def get_inbox_messages(self, limit=10):
        """
        Retrieve private messages from the inbox.
        :param limit: Number of messages to retrieve
        :return: List of messages or error message
        """
        try:
            inbox_messages = list(self.reddit.inbox.messages(limit=limit))
            logger.info(f"Retrieved {len(inbox_messages)} messages from inbox")
            return inbox_messages
        except Exception as e:
            logger.error(f"Error retrieving inbox messages: {e}")
            return {"error": str(e)}

    def get_sent_messages(self, limit=10):
        """
        Retrieve sent private messages.
        :param limit: Number of sent messages to retrieve
        :return: List of sent messages or error message
        """
        try:
            sent_messages = list(self.reddit.inbox.sent(limit=limit))
            logger.info(f"Retrieved {len(sent_messages)} sent messages")
            return sent_messages
        except Exception as e:
            logger.error(f"Error retrieving sent messages: {e}")
            return {"error": str(e)}

    def create_collection(self, subreddit, title):
        """
        Create a new collection in a subreddit.
        :param subreddit: The subreddit to create the collection in
        :param title: Title of the collection
        :return: Collection details or error message
        """
        try:
            collection = self.reddit.subreddit(subreddit).collections.create(title=title)
            logger.info(f"Created collection '{title}' in r/{subreddit}")
            return collection
        except Exception as e:
            logger.error(f"Error creating collection in r/{subreddit}: {e}")
            return {"error": str(e)}

    def delete_collection(self, subreddit, collection_id):
        """
        Delete a collection from a subreddit.
        :param subreddit: The subreddit containing the collection
        :param collection_id: ID of the collection to delete
        :return: Success or error message
        """
        try:
            self.reddit.subreddit(subreddit).collections.delete(collection_id=collection_id)
            logger.info(f"Deleted collection with ID {collection_id} from r/{subreddit}")
            return {"status": "Collection deleted"}
        except Exception as e:
            logger.error(f"Error deleting collection from r/{subreddit}: {e}")
            return {"error": str(e)}

    def reorder_collection(self, subreddit, collection_id, link_ids):
        """
        Reorder posts within a collection.
        :param subreddit: The subreddit containing the collection
        :param collection_id: ID of the collection to reorder
        :param link_ids: List of post IDs in the desired order
        :return: Success or error message
        """
        try:
            self.reddit.subreddit(subreddit).collections.reorder(
                collection_id=collection_id, link_ids=link_ids
            )
            logger.info(f"Reordered collection {collection_id} in r/{subreddit}")
            return {"status": "Collection reordered"}
        except Exception as e:
            logger.error(f"Error reordering collection in r/{subreddit}: {e}")
            return {"error": str(e)}

    def get_subreddit_emojis(self, subreddit):
        """
        Retrieve all custom emojis from a subreddit.
        :param subreddit: Subreddit name
        :return: List of emojis or error message
        """
        try:
            emojis = self.reddit.subreddit(subreddit).emoji
            logger.info(f"Retrieved {len(emojis)} emojis from r/{subreddit}")
            return list(emojis)
        except Exception as e:
            logger.error(f"Error retrieving emojis from r/{subreddit}: {e}")
            return {"error": str(e)}
    def get_all_subreddit_emojis(self, subreddit):
        """
        Retrieve all emojis for a subreddit.
        :param subreddit: Subreddit name
        :return: List of emojis or error message
        """
        try:
            emojis = self.reddit.subreddit(subreddit).emoji
            logger.info(f"Retrieved {len(emojis)} emojis from r/{subreddit}")
            return list(emojis)
        except Exception as e:
            logger.error(f"Error retrieving emojis from r/{subreddit}: {e}")
            return {"error": str(e)}

    def set_user_flair(self, subreddit, username, flair_text, flair_template_id=None):
        """
        Set user flair for a subreddit.
        :param subreddit: Subreddit name
        :param username: Username to assign flair to
        :param flair_text: Text to set as the user's flair
        :param flair_template_id: Flair template ID, optional
        :return: Success or error message
        """
        try:
            self.reddit.subreddit(subreddit).flair.set(
                redditor=username, text=flair_text, flair_template_id=flair_template_id
            )
            logger.info(f"Set user flair for {username} in r/{subreddit}")
            return {"status": "User flair set"}
        except Exception as e:
            logger.error(f"Error setting user flair for {username} in r/{subreddit}: {e}")
            return {"error": str(e)}

    def set_link_flair(self, subreddit, submission_id, flair_text, flair_template_id):
        """
        Assign flair to a link (post) in a subreddit.
        :param subreddit: Subreddit name
        :param submission_id: Submission ID of the post
        :param flair_text: Text to set as the link's flair
        :param flair_template_id: Flair template ID
        :return: Success or error message
        """
        try:
            submission = self.reddit.submission(submission_id)
            submission.flair.select(flair_template_id=flair_template_id, text=flair_text)
            logger.info(f"Set link flair for submission {submission_id} in r/{subreddit}")
            return {"status": "Link flair set"}
        except Exception as e:
            logger.error(f"Error setting link flair for {submission_id} in r/{subreddit}: {e}")
            return {"error": str(e)}

    def list_wiki_pages(self, subreddit):
        """
        List all pages in a subreddit's wiki.
        :param subreddit: Subreddit name
        :return: List of wiki pages or error message
        """
        try:
            wiki_pages = self.reddit.subreddit(subreddit).wiki.pages
            logger.info(f"Retrieved {len(wiki_pages)} wiki pages in r/{subreddit}")
            return list(wiki_pages)
        except Exception as e:
            logger.error(f"Error listing wiki pages in r/{subreddit}: {e}")
            return {"error": str(e)}

    def edit_wiki_page(self, subreddit, page, content):
        """
        Edit a wiki page in a subreddit.
        :param subreddit: Subreddit name
        :param page: Wiki page name
        :param content: New content for the wiki page
        :return: Success or error message
        """
        try:
            wiki_page = self.reddit.subreddit(subreddit).wiki[page]
            wiki_page.edit(content=content)
            logger.info(f"Edited wiki page '{page}' in r/{subreddit}")
            return {"status": "Wiki page edited"}
        except Exception as e:
            logger.error(f"Error editing wiki page '{page}' in r/{subreddit}: {e}")
            return {"error": str(e)}

    def get_wiki_page_discussions(self, subreddit, page):
        """
        Retrieve discussions for a wiki page.
        :param subreddit: Subreddit name
        :param page: Wiki page name
        :return: List of discussions or error message
        """
        try:
            discussions = self.reddit.subreddit(subreddit).wiki[page].discussions
            logger.info(f"Retrieved {len(discussions)} discussions for wiki page '{page}' in r/{subreddit}")
            return list(discussions)
        except Exception as e:
            logger.error(f"Error retrieving discussions for wiki page '{page}' in r/{subreddit}: {e}")
            return {"error": str(e)}

