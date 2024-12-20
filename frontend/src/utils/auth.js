export const setDomain = (tenant_domain) => {
  localStorage.setItem("tenant_domain", tenant_domain);
};

export const getDomain = () => {
  return localStorage.getItem("tenant_domain");
};

export const removeDomain = () => {
  localStorage.removeItem("tenant_domain");
};

export const setToken = (token) => {
  localStorage.setItem("access_token", token);
};

export const getToken = () => {
  return localStorage.getItem("access_token");
};

export const removeToken = () => {
  localStorage.removeItem("access_token");
};

export const isAuthenticated = () => {
  return !!getToken();
};
