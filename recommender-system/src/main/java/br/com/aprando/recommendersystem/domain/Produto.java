package br.com.aprando.recommendersystem.domain;

import java.util.HashMap;
import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "produto")
public class Produto {

	@Id
	private String id;

	private Long sku;

	private String nome;

	private String fonte;

	private String descricaoLonga;

	private String descricaoLongaHtml;

	private String descricaoCurta;

	private String descricaoCurtaHtml;

	private String image;

	private Double preco;
	
	private Double cosineSimilarity;

	private List<String> categorias;

	private List<String> caracteristicas;

	private HashMap<String, String> detalhes;
	
	public Double getCosineSimilarity() {
		return cosineSimilarity;
	}

	public void setCosineSimilarity(Double cosineSimilarity) {
		this.cosineSimilarity = cosineSimilarity;
	}

	public List<String> getCategorias() {
		return categorias;
	}

	public void setCategorias(List<String> categorias) {
		this.categorias = categorias;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public Long getSku() {
		return sku;
	}

	public void setSku(Long sku) {
		this.sku = sku;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getFonte() {
		return fonte;
	}

	public void setFonte(String fonte) {
		this.fonte = fonte;
	}

	public String getDescricaoLonga() {
		return descricaoLonga;
	}

	public void setDescricaoLonga(String descricaoLonga) {
		this.descricaoLonga = descricaoLonga;
	}

	public String getDescricaoLongaHtml() {
		return descricaoLongaHtml;
	}

	public void setDescricaoLongaHtml(String descricaoLongaHtml) {
		this.descricaoLongaHtml = descricaoLongaHtml;
	}

	public String getDescricaoCurta() {
		return descricaoCurta;
	}

	public void setDescricaoCurta(String descricaoCurta) {
		this.descricaoCurta = descricaoCurta;
	}

	public String getDescricaoCurtaHtml() {
		return descricaoCurtaHtml;
	}

	public void setDescricaoCurtaHtml(String descricaoCurtaHtml) {
		this.descricaoCurtaHtml = descricaoCurtaHtml;
	}
	
	public String getImage() {
		return image;
	}

	public void setImage(String image) {
		this.image = image;
	}

	public Double getPreco() {
		return preco;
	}

	public void setPreco(Double preco) {
		this.preco = preco;
	}


	public List<String> getCaracteristicas() {
		return caracteristicas;
	}

	public void setCaracteristicas(List<String> caracteristicas) {
		this.caracteristicas = caracteristicas;
	}

	public HashMap<String, String> getDetalhes() {
		return detalhes;
	}

	public void setDetalhes(HashMap<String, String> detalhes) {
		this.detalhes = detalhes;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((id == null) ? 0 : id.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Produto other = (Produto) obj;
		if (id == null) {
			if (other.id != null)
				return false;
		} else if (!id.equals(other.id))
			return false;
		return true;
	}
	
	

}
