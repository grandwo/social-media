CREATE TRIGGER after_friend_delete
AFTER DELETE ON friends
FOR EACH ROW
BEGIN
    DELETE FROM friends
    WHERE user_id = OLD.friend_id AND friend_id = OLD.user_id;

    DELETE FROM friend_group_members
    WHERE friend_id = OLD.friend_id
    AND group_id IN (
        SELECT group_id FROM friend_groups WHERE user_id = OLD.user_id
    );

    DELETE FROM friend_group_members
    WHERE friend_id = OLD.user_id
    AND group_id IN (
        SELECT group_id FROM friend_groups WHERE user_id = OLD.friend_id
    );
END;
