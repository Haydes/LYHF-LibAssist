package com.team.service;

import com.team.dao.UserDao;
import com.team.entity.User;

public class UserService {
	private UserDao userDao = new UserDao();
	
	public User login(String name, String password) {
		User user = userDao.findByName(name);
		if (user == null) {
			return null;
		}
		
		if (!password.equals(user.getPassword())) {
			return null;
		}
		
		return user;
	}
}
