package com.team.dao;

import java.sql.SQLException;

import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;

import com.team.entity.User;
import com.team.utils.C3P0Util;


public class UserDao {
	private QueryRunner runner = new QueryRunner(C3P0Util.getDs());

	public User findByName(String name) {
		try {
			return runner.query("select * from user where name=?", new BeanHandler<User>(User.class), name);

		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
	}
}
