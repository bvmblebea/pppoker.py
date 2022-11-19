import requests
from uuid import uuid4
from hashlib import md5
from random import randint

class PPPoker:
	def __init__(
			self,
			app_id: str = "globle", 
			app_type: int = 1,
			language: str = "ru",
			platform: str = "android",
			region: int = 2,
			country: str = "RU") -> None:
		self.api = "http://www.pppoker.club"
		self.headers = {
			"user-agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"}
		self.rd_key = None
		self.user_id = None
		self.app_id = app_id
		self.region = region
		self.country = country
		self.app_type = app_type
		self.language = language
		self.platform = platform
		self.imei = self.generate_imei()
		self.version = self.get_client_version()["latest_version"]

	def md5hash(self, string: str) -> str:
		return md5(md5(string.encode()).hexdigest().encode()).hexdigest()

	def generate_imei(self) -> int:
		return randint(1000_0000_0000_000, 9000_0000_0000_000)

	def get_client_version(self) -> dict:
		return requests.get(
			f"{self.api}/poker/api/version.php",
			headers=self.headers).json()

	def login(
			self, 
			username: str, 
			password: str, 
			type: int = 4) -> dict:
		data = {
			"app_type": self.app_type,
			"appid": self.app_id,
			"apple_full_name": "nil",
			"apple_identity_token": "nil",
			"apple_user": "nil",
			"clientvar": self.version,
			"country": self.country,
			"distributor": 0,
			"imei": self.imei,
			"lang": self.language,
			"languagecode": self.language,
			"operating_company": self.platform,
			"os": self.platform,
			"password": self.md5hash(password),
			"platform_type": 2,
			"region": self.region,
			"sub_distributor": 0,
			"type": type,
			"username": username
		}
		response = requests.post(
			f"{self.api}/poker/api/login.php", 
			data=data, 
			headers=self.headers).json()
		if "uid" in response:
			self.user_id = response["uid"]
			self.rd_key = response["rdkey"]
		return response

	def register(
			self,
			username: str,
			password: str) -> dict:
		return requests.get(
			f"{self.api}/poker/api/register.php?username={username}&password={self.md5hash(password)}&distributor=0&sub_distributor=0&country={self.country}&appid={self.app_id}&os={self.platform}&imei={self.imei}&clientvar={self.version}&ad_id={uuid4()}&region={self.region}&app_type={self.app_type}",
			headers=self.headers).json()

	def get_verification_code(self, email: str, valid_type: int = 1) -> dict:
		return requests.get(
			f"{self.api}/poker/api/mail/send_valid_code.php?mail={email}&valid_type={valid_type}&lang={self.language}",
			headers=self.headers).json()

	def edit_profile(self, country: str) -> dict:
		data = {
			"country": country,
			"rdkey": self.rd_key,
			"uid": self.user_id
		}
		return requests.post(
			f"{self.api}/poker/api/modify_userinfo.php",
			data=data,
			headers=self.headers).json()

	def get_portrait_list(self) -> dict:
		return requests.get(
			f"{self.api}/poker-api/portrait/list?uid={self.user_id}&rdkey={self.rd_key}",
			headers=self.headers).json()

	def change_portrait(self, icon_name: str) -> dict:
		data = {
			"icon_name": icon_name,
			"rdkey": self.rd_key,
			"uid": self.user_id
		}
		return requests.post(
			f"{self.api}/poker-api/portrait/choice",
			data=data,
			headers=self.headers).json()

	def get_user_invite_code(self) -> dict:
		return requests.get(
			f"{self.api}/server_api/user_invite/code?uid={self.user_id}&rdkey={self.rd_key}",
			headers=self.headers).json()

	def get_user_tasks(self) -> dict:
		return requests.get(
			f"{self.api}/server_api/new_user_task/tasks?uid={self.user_id}&rdkey={self.rd_key}",
			headers=self.headers).json()

	def link_email(
			self,
			email: str,
			verification_code: int) -> dict:
		return requests.get(
			f"{self.api}/poker/api/mail/valid_mail.php?mail={email}&valid_code={verification_code}&rdkey={self.rd_key}&uid={self.user_id}",
			headers=self.headers).json()

	def unlink_email(self, email: str, password: str) -> dict:
		return requests.get(
			f"{self.api}/poker/api/mail/unlink_mail.php?mail={email}&password={self.md5hash(password)}&uid={self.user_id}",
			headers=self.headers).json()

	def change_password(
			self,
			new_password: str,
			old_password: str) -> dict:
		return requests.get(
			f"{self.api}/poker/api/mail/change_pw.php?uid={self.user_id}&password={self.md5hash(new_password)}&old_password={self.md5hash(old_password)}",
			headers=self.headers).json()

	def get_ip_address(self) -> dict:
		return requests.get(
			f"{self.api}/poker/api/getip.php", 
			headers=self.headers).json()

	def check_username(self, username: str) -> dict:
		return requests.get(
			f"{self.api}/poker/api/check_username.php?username={username}",
			headers=self.headers).json()
