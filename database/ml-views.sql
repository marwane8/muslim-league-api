-- -----------------------------------------------------
-- Roster View 
-- -----------------------------------------------------
CREATE VIEW `roster` AS
    SELECT 
        `players`.`player_id` AS `id`,
        `teams`.`team_id` AS `team_id`,
        `teams`.`team_name` AS `team_name`,
        `players`.`player_name` AS `player_name`,
        `players`.`player_number` AS `player_number`,
        `players`.`player_pos` AS `player_pos`
    FROM
        ((`teams_players` `tp`
        LEFT JOIN `teams` ON ((`tp`.`team_id` = `teams`.`team_id`)))
        LEFT JOIN `players` ON ((`tp`.`player_id` = `players`.`player_id`)))

-- Example Select Statement
SELECT * FROM roster WHERE team_id=16;

-- -----------------------------------------------------
-- Schedule View 
-- -----------------------------------------------------
CREATE VIEW `schedule` AS
    SELECT
        `games`.`game_id` AS `game_id`,
        `games`.`team1_id` AS `team1_id`,
        `tm1`.`team_name` AS `team1`,
        `games`.`team2_id` AS `team2_id`,
        `tm2`.`team_name` AS `team2`,
        `games`.`date` AS `date`,
        `games`.`start_time` AS `start_time`,
        `l`.`court` AS `court`,
        `games`.`playoff` AS `playoff` 
    from 
        (((`games` 
        left join `teams` `tm1` on((`games`.`team1_id` = `tm1`.`team_id`))) 
        left join `location` `l` on((`games`.`location_id` = `l`.`location_id`))) 
        left join `teams` `tm2` on((`games`.`team2_id` = `tm2`.`team_id`)));


-- -----------------------------------------------------
-- Game Totals 
-- -----------------------------------------------------
CREATE VIEW `game_totals` AS
    SELECT 
        `teams`.`team_id` AS `t_id`,
        `teams`.`team_name` AS `team_name`,
        `statistics`.`game_id` AS `g_id`,
        sum(`statistics`.`points`) AS `total_pts`,
        sum(`statistics`.`rebounds`) AS `total_reb`,
        sum(`statistics`.`fouls`) AS `fls`
    FROM
        (((`teams_players` `tp`
        LEFT JOIN `teams` ON ((`tp`.`team_id` = `teams`.`team_id`)))
        LEFT JOIN `players` ON ((`tp`.`player_id` = `players`.`player_id`)))
        LEFT JOIN `statistics` ON (`tp`.`player_id` = `statistics`.`player_id`))
        GROUP BY `t_id`,`g_id`;

-- -----------------------------------------------------
-- Game Totals 
-- -----------------------------------------------------
CREATE VIEW `team_totals` AS
    SELECT 
        `teams`.`team_id` AS `t_id`,
        `teams`.`team_name` AS `team_name`,
        `statistics`.`game_id` AS `g_id`,
        sum(`statistics`.`points`) AS `total_pts`,
        sum(`statistics`.`rebounds`) AS `total_reb`,
        sum(`statistics`.`fouls`) AS `fls`
    FROM
        (((`teams_players` `tp`
        LEFT JOIN `teams` ON ((`tp`.`team_id` = `teams`.`team_id`)))
        LEFT JOIN `players` ON ((`tp`.`player_id` = `players`.`player_id`)))
        LEFT JOIN `statistics` ON (`tp`.`player_id` = `statistics`.`player_id`))
        GROUP BY `t_id`;


-- -----------------------------------------------------
-- Player Totals 
-- -----------------------------------------------------
CREATE  VIEW `player_totals` AS 
    select 
        `st`.`player_id` AS `p_id`,
        `players`.`player_name` AS `name`,
        Count(*) AS `games_played`,
        sum(`st`.`points`) AS `points`,
        sum(`st`.`rebounds`) AS `rebounds`,
        sum(`st`.`fouls`) AS `fouls`
    from 
        (`statistics` `st` 
        left join `players` on((`st`.`player_id` = `players`.`player_id`))) 
        group by `p_id`;

