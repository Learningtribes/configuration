cfg = rs.conf();
cfg.members[0].host="127.0.0.1:27017";
rs.reconfig(cfg);