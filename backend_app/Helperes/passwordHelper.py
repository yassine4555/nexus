import hashlib
from modeles.passwordSecuirity import passwordSecurity
from testStore import json_user_password_store
from testStore.json_user_password_store import JsonUserPasswordStore


class passwordHelper:


    @staticmethod
    def EncrpytingPassword(password):
        return hashlib.sha512(password.encode()).hexdigest()

    @staticmethod
    def CompareHashPasswordandPassword(hashedPassword, plainPassword):

        return hashedPassword == passwordHelper.EncrpytingPassword(plainPassword)

    @staticmethod
    def assignPasswordToUser(userId, password):
        jsonPass= JsonUserPasswordStore("./passJson.json")
        encryptedPassword = passwordHelper.EncrpytingPassword(password)
        ##SecuirityClass = passwordSecurity(encryptedPassword, userId)
        jsonPass.set_password(userId, encryptedPassword)


    @staticmethod
    def isPasswordTrueForUser(userid, password):
        #get hashed password from db by user id


        hashedPassword = passwordHelper.getPasswordForUser(userid)
        print(hashedPassword)
        return passwordHelper.CompareHashPasswordandPassword(hashedPassword, password)

    @staticmethod
    def getPasswordForUser(userid):
        #get hashed password from db by user id
        json_user_password_store = JsonUserPasswordStore("./passJson.json")
        hashedPassword = json_user_password_store.get_password(userid)
        # Replace with actual retrieval logic
        return hashedPassword