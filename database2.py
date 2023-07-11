import pandas as pd

class UserNode:
    def __init__(self, id, name, last_name):
        self.id = id
        df_account = pd.DataFrame({'name':[name],'last_name':[last_name]})
        df_personal_events = pd.DataFrame({'name':[],'date_ini':[],'date_end':[],'visibility':[]})
        df_groups = pd.DataFrame({'name':[],'id_group':[],'role':[]})
        df_groupal_events = pd.DataFrame({'name':[],'date_ini':[],'date_end':[]})
        dataframes = [df_account,df_personal_events,df_groups,df_groupal_events]
        dataframes = pd.DataFrame({'info_personal':dataframes}, index=['account','personal_events','groups','groupal_events'])
        self.information = pd.DataFrame({'info_users':[dataframes]},index=[id])
        
    def delete_account(self):
        self.information.drop(self.id, inplace=True)

    def merge_users(self, other):
        df1 = self.information
        df2 = other.information
        self.information = df1.append(df2)

    def diverge_users(self, other):
        # df1 = self.information
        # df2 = other.information
        # self.information = df1.append(df2)
        pass
    
    def create_personal_event(self, name, date_ini, date_end, visibility="private"):
        df = self.information.loc[self.id,'info_users'].loc['personal_events','info_personal']
        index = df.index.max() if not df.empty else -1
        df.loc[index+1,'name'] = name
        df.loc[index+1,'date_ini'] = date_ini
        df.loc[index+1,'date_end'] = date_end
        df.loc[index+1,'visibility'] = visibility

    def modifiy_personal_event(self, id_event, name=None, date_ini=None, date_end=None, visibility=None):
        df = self.information.loc[self.id,'info_users'].loc['personal_events','info_personal']
        df.loc[id_event,'name'] = name if name else df.loc[id_event,'name']
        df.loc[id_event,'date_ini'] = date_ini if date_ini else df.loc[id_event,'date_ini']
        df.loc[id_event,'date_end'] = date_end if date_end else df.loc[id_event,'date_end']
        df.loc[id_event,'visibility'] = visibility if visibility else df.loc[id_event,'visibility']
    
    def delete_personal_event(self, id_event):
        df = self.information.loc[self.id,'info_users'].loc['personal_events','info_personal']
        df.drop(id_event, inplace=True)

    def create_group(self, name, propietary, type_group):
        pass

    def delete_group(self):
        pass

    def add_role_to_group(self):
        pass

    def delete_role_from_group(self):
        pass

    def add_member(self):
        pass

    def delete_member(self):
        pass

    def modify_role_to_member(self):
        pass

    def create_groupal_event(self):
        pass

    def modify_groupal_event(self):
        pass

    def delete_groupal_event(self):
        pass


user = UserNode("23345552333","Jordan", "Pla Glez")
user.create_personal_event('Boda de Tia' ,'23/4/34','23/45/42', 'public')
user.modifiy_personal_event(0, visibility='private')
user.create_personal_event('Cumple de Tia' ,'28/4/34','28/45/42', 'public')
user.create_personal_event('Boda de Hermana' ,'31/4/34','31/45/42', 'public')
user.delete_personal_event(1)
user2 = UserNode("23345552334","Diane", "Cruz Mengana")
user2.create_personal_event('Boda de Tia' ,'23/4/34','23/45/42', 'public')
user2.modifiy_personal_event(0, visibility='private')
user2.create_personal_event('Cumple de Hermana' ,'31/4/34','31/45/42', 'public')
user.merge_users(user2)
user.delete_account()