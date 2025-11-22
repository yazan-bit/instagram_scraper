from analyzer import InstagramAnalyzer,InstagramDataSaver

def main():
    username = input("enter your username")
    analyzer = InstagramAnalyzer(username) 
    saver = InstagramDataSaver(username)
    try:
        # Setup driver
        analyzer.setup_driver()
        
        # Login
        if analyzer.login():
            # Menu system
            followers = analyzer.get_my_followers_list()
            following = analyzer.get_my_following_list()
            friends = followers & following
            not_friends = following - followers

            saver.save_to_json(followers,following,friends,not_friends)
            saver.save_summary_report(followers,following,friends,not_friends)

        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()