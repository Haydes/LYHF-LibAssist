package com.team.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.team.entity.User;
import com.team.service.UserService;


public class UserServlet extends HttpServlet {
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		resp.setContentType("text/html");
		PrintWriter out = resp.getWriter();
		
		String name = req.getParameter("name");
		String password = req.getParameter("password");
		
		UserService userService = new UserService();
		User user = userService.login(name, password);
		if (user == null) {
			out.print("<h1>login failed</h1>");
			out.print("<a href='login.html'>login again</a>");
		} else {
			out.print("<h1>welcome!</h1>");
			out.print("<h2>"+ name + "</h2>");
		}
		out.close();
	}

	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		doGet(req, resp);
	}
}
