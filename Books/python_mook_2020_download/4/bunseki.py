%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from sklearn import linear_model

SERVICE_NUM = 2 # ���͑Ώۂ̃t���}�T�[�r�X�̐�
ITEM_NUM = 3 # ���͑Ώۂ̏��i�̐�
RECENT_DAYS = 5 # ���߂ŕ��͂������

register_matplotlib_converters()

# �O���t�̃T�C�Y�ݒ�
plt.figure(figsize=(15, 18))

# ���`��A���f������
clf = linear_model.LinearRegression()

# CSV�ǂݍ��݁B1��ڂ͓��t�^�œǂݍ��݁A�C���f�b�N�X�Ƃ���
df= pd.read_csv('data.csv',index_col=0, parse_dates=True)

# �����ϐ��ݒ�
X = df.index.to_frame() # �S��
X_recent = X.tail(RECENT_DAYS) # ����

# �v���b�g��̔ԍ���������
no = 1

# ���i���ƂɃ����J���ƃ��N�}�̃f�[�^���͂ƃO���t�쐬
for i, (col_name, Y) in enumerate(df.iteritems()):
    # �����J���ƃ��N�}��2�񂲂Ɠ����O���t�Ƀv���b�g
    if i % SERVICE_NUM == 0:
        plt.subplot(ITEM_NUM, 1, no) # �v���b�g���ݒ�
        plt.title('item' + str(no)) # �^�C�g��
    else:
        no += 1 # �v���b�g���1�i�߂�

    # �S���̃O���t�쐬
    plt.plot(X, Y, label=col_name)

    # �S���ŕ���
    clf.fit(X, Y) # �w�K
    plt.plot(X, clf.predict(X.values.astype(float)),
        linestyle='dashed', label=col_name + '_reg') # ��A�����`��

    # ���߂ŕ���
    clf.fit(X_recent, Y.tail(RECENT_DAYS)) # �w�K
    label_recent = f'{col_name}_reg_recent_{RECENT_DAYS}days'
    plt.plot(X_recent, clf.predict(X_recent.values.astype(float)),
        linestyle='dotted', label=label_recent) # ��A�����`��

    plt.legend() # �}��\��

plt.show()