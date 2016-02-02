package br.com.aprando.recommendersystem.domain;

import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "recomendacao")
public class Recomendacao {

	@Id
	private String id;
	
	private String userId;
	
	private String postId;
	
	private String post;
	
	private String resource;

	private List<Produto> products;

	private Double cosineSimilarity;
	
	private Double rate;
	
	public String getUserId() {
		return userId;
	}

	public void setUserId(String userId) {
		this.userId = userId;
	}

	public String getPostId() {
		return postId;
	}

	public void setPostId(String postId) {
		this.postId = postId;
	}

	public String getPost() {
		return post;
	}

	public void setPost(String post) {
		this.post = post;
	}

	public String getResource() {
		return resource;
	}

	public void setResource(String resource) {
		this.resource = resource;
	}

	public List<Produto> getProducts() {
		return products;
	}

	public void setProducts(List<Produto> products) {
		this.products = products;
	}

	public Double getCosineSimilarity() {
		return cosineSimilarity;
	}

	public void setCosineSimilarity(Double cosineSimilarity) {
		this.cosineSimilarity = cosineSimilarity;
	}

	public Double getRate() {
		return rate;
	}

	public void setRate(Double rate) {
		this.rate = rate;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

}
