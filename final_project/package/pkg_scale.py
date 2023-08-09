import pymssql

def get_itemcode():
    rows = []
    con = pymssql.connect(#server="192.168.0.112:1433",
                    #   host='localhost',
                      server = "222.235.141.8:1111",
                      database="KDTB03_1JO",
                      user="KDTB03",
                      password="333538",
                      charset = "EUC-KR") # 글자 꺠짐 방지

    cur=con.cursor()
    sql = ""
    sql += "  SELECT ITEMCODE "
    sql += "        ,ITEMNAME "
    sql += "    FROM TB_ItemMaster "
    sql += "ORDER BY ITEMNAME, ITEMCODE "
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    new_list = []
    for i,j in rows:
        new_list.append(i)
        new_list.append(j)
    # new_list = [item[0] for item in rows]
    return new_list

def get_current(selected_option):
    rows = []
    con = pymssql.connect(#server="192.168.0.112:1433",
                    #   host='localhost',
                      server = "222.235.141.8:1111",
                      database="KDTB03_1JO",
                      user="KDTB03",
                      password="333538",
                      charset = "EUC-KR") # 글자 꺠짐 방지
    cur=con.cursor()
    sql = ""
    sql += "   SELECT A.ITEMCODE, B.CUR_STOCKQTY, A.SAFESTOCK, A.APPRSTOCK"
    sql += " FROM TB_ItemMaster A WITH(NOLOCK) LEFT JOIN (SELECT SUM(STOCKQTY) AS CUR_STOCKQTY"
    sql += "									             ,ITEMCODE"
    sql += "								    	     FROM TB_StockMM"
    sql += f"								    		WHERE ITEMCODE = '{selected_option}'"
    sql += "								    	 GROUP BY ITEMCODE) B "
    sql += "								       ON A.ITEMCODE = B.ITEMCODE"
    sql += f" WHERE A.ITEMCODE = '{selected_option}'"
    
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    new_list = []
    for i in range(len(rows)):
        new_list.append(rows[i])
    return new_list

def autu_enroll(input_data):
    con = pymssql.connect(#server="192.168.0.112:1433",
                    #   host='localhost',
                      server = "222.235.141.8:1111",
                      database="KDTB03_1JO",
                      user="KDTB03",
                      password="333538",
                      charset = "EUC-KR") # 글자 꺠짐 방지
    cur=con.cursor()

    sql = ""
    sql += " SELECT AORDERFLAG "
    sql += "   FROM TB_ItemMaster "
    sql += f" WHERE ITEMCODE = '{input_data}' "
    cur.execute(sql)
    rows = cur.fetchone()
    con.close()
    try:
        s = ''.join(rows)
    except:
        s = 'N'
    
    con = pymssql.connect(#server="192.168.0.112:1433",
                #   host='localhost',
                  server = "222.235.141.8:1111",
                  database="KDTB03_1JO",
                  user="KDTB03",
                  password="333538",
                  charset = "EUC-KR")
    cur = con.cursor()
    sql = ""
    if (s == 'Y'):   # TB_MaterialOrder에 insert 로직 시행
        sql += " DECLARE @LD_NOWDATE DATETIME "
        sql += "        ,@LS_NOWDATE VARCHAR(10) "
        sql += "        ,@LI_SEQ     INT "
        sql += "        ,@LS_PONO    VARCHAR(20) "
        sql += "        ,@LS_MAKER   VARCHAR(10) "
        sql += " SET @LD_NOWDATE = GETDATE() "
        sql += " SET @LS_NOWDATE = CONVERT(VARCHAR,@LD_NOWDATE,23) "
        sql += " SELECT @LI_SEQ = ISNULL(MAX(POSEQ),0) + 1 "
        sql += "   FROM TB_MaterialOrder WITH (NOLOCK) "
        sql += "  WHERE PLANTCODE = '1000' "
        sql += "    AND PODATE    = @LS_NOWDATE "
        sql += " SET @LI_SEQ = ISNULL(@LI_SEQ,1) "
        sql += " SET @LS_PONO = 'PO' + CONVERT(VARCHAR,@LD_NOWDATE,112) + RIGHT('00000' + CONVERT(VARCHAR,@LI_SEQ),4) "
        sql += " SELECT @LS_MAKER = B.WORKERNAME "
        sql += "   FROM TP_WorkcenterStatus A WITH(NOLOCK) JOIN TB_WorkerList B WITH(NOLOCK) "
        sql += "                                             ON A.WORKER = B.WORKERID "
        sql += "  WHERE A.PLANTCODE = '1000' "
        sql += "    AND A.WORKCENTERCODE = 'WO07_ASSY' "
        sql += "   INSERT INTO TB_MaterialOrder (PLANTCODE, PONO,     ITEMCODE,       PODATE,      POQTY, UNITCODE, MAKER,     MAKEDATE,    CUSTCODE, POSEQ,  AORDERSTATUS) "
        sql += f"                        VALUES ('1000',    @LS_PONO, '{input_data}', @LS_NOWDATE, 1000,  'EA',     @LS_MAKER, @LD_NOWDATE, 'C3001', @LI_SEQ, 'Y') "
    else:
        sql += " DECLARE @LD_NOWDATE DATETIME  "
        sql += "        ,@LS_NOWDATE VARCHAR(10)  "
        sql += "        ,@LI_ReqSEQ  INT  "
        sql += "        ,@LS_MAKER   VARCHAR(10)  "
        sql += " SET @LD_NOWDATE = GETDATE()  "
        sql += " SET @LS_NOWDATE = CONVERT(VARCHAR,@LD_NOWDATE,23)  "
        sql += " SELECT @LI_ReqSEQ = ISNULL(MAX(ReqSEQ), 0) + 1  "
        sql += "   FROM TB_OrderRequestList WITH(NOLOCK)  "
        sql += "  WHERE PLANTCODE = '1000'  "
        sql += "    AND ReqDATE   = @LS_NOWDATE  "
        sql += " SELECT @LS_MAKER = B.WORKERNAME  "
        sql += "   FROM TP_WorkcenterStatus A WITH(NOLOCK) JOIN TB_WorkerList B WITH(NOLOCK)  "
        sql += "                                             ON A.WORKER = B.WORKERID  "
        sql += "  WHERE A.PLANTCODE = '1000'  "
        sql += "    AND A.WORKCENTERCODE = 'WO07_ASSY'  "
        sql += " INSERT INTO TB_OrderRequestList (PLANTCODE, ReqSEQ,     ReqDATE,     ITEMCODE, ReqQTY,   UNITCODE, CUSTCODE, ApprSTATUS, MAKER,     MAKEDATE)  "
        sql += f"                          VALUES('1000'   , @LI_ReqSEQ, @LS_NOWDATE, '{input_data}', 1000,    'EA'    , 'C3001',  'N'       , @LS_MAKER, @LD_NOWDATE)"
        
    cur.execute(sql)
    con.commit()
    con.close()
    return s